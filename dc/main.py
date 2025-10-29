import datetime as dt
from functools import partial
from math import floor, isnan

import js
import pandas as pd
from pyodide.ffi import to_js
from pyscript.js_modules import d3, dc
from pyscript.js_modules.crossfilter import default as crossfilter


def year_add(p, v, _nf):
    p["count"] += 1
    p["absGain"] += v.close - v.open
    p["fluctuation"] += abs(v.close - v.open)
    p["sumIndex"] += (v.open + v.close) / 2
    p["avgIndex"] = p["sumIndex"] / p["count"]
    p["percentageGain"] = (p["absGain"] / p["avgIndex"]) * 100 if p["avgIndex"] else 0
    p["fluctuationPercentage"] = (
        (p["fluctuation"] / p["avgIndex"]) * 100 if p["avgIndex"] else 0
    )
    return p


def year_remove(p, v, _nf):
    p["count"] -= 1
    p["absGain"] -= v.close - v.open
    p["fluctuation"] -= abs(v.close - v.open)
    p["sumIndex"] -= (v.open + v.close) / 2
    p["avgIndex"] = p["sumIndex"] / p["count"] if p["count"] else 0
    p["percentageGain"] = (p["absGain"] / p["avgIndex"]) * 100 if p["avgIndex"] else 0
    p["fluctuationPercentage"] = (
        (p["fluctuation"] / p["avgIndex"]) * 100 if p["avgIndex"] else 0
    )
    return p


def year_initialize():
    return {
        "count": 0,
        "absGain": 0.0,
        "fluctuation": 0.0,
        "fluctuationPercentage": 0.0,
        "sumIndex": 0.0,
        "avgIndex": 0.0,
        "percentageGain": 0.0,
    }


def month_add(p, v, _nf):
    p["days"] += 1
    p["total"] += (v.open + v.close) / 2
    p["avg"] = round(p["total"] / p["days"])
    return p


def month_remove(p, v, _nf):
    p["days"] -= 1
    p["total"] -= (v.open + v.close) / 2
    p["avg"] = round(p["total"] / p["days"]) if p["days"] else 0
    return p


def month_initialize():
    return {"days": 0, "total": 0.0, "avg": 0.0}


def gainOrLossLabel(d):
    label = d.key
    if gainOrLossChart.hasFilter() and not gainOrLossChart.hasFilter(label):
        return f"{label}(0%)"
    total = all.value()
    if total:
        label += f"({d.value / total * 100:.0f}%)"
    return label


def moveTitle(d, _):
    value = d.value
    value = value["avg"] if isinstance(value, dict) else value
    if isnan(value):
        value = 0
    return f"{dateFormat(d.key)}\n{value:{numberFormat}}"


def filter_all(charts, *_):
    for chart in charts:
        chart.filterAll()
    dc.redrawAll()


def reset_all(*_):
    dc.filterAll()
    dc.renderAll()


gainOrLossChart = dc.pieChart("#gain-loss-chart")
fluctuationChart = dc.barChart("#fluctuation-chart")
quarterChart = dc.pieChart("#quarter-chart")
dayOfWeekChart = dc.rowChart("#day-of-week-chart")
moveChart = dc.lineChart("#monthly-move-chart")
volumeChart = dc.barChart("#monthly-volume-chart")
yearlyBubbleChart = dc.bubbleChart("#yearly-bubble-chart")
nasdaqCount = dc.dataCount(".dc-data-count")
nasdaqTable = dc.dataTable(".dc-data-table")

for chart in [
    yearlyBubbleChart,
    gainOrLossChart,
    quarterChart,
    dayOfWeekChart,
    fluctuationChart,
]:
    chart.select("a").on("click", to_js(partial(filter_all, [chart])))
moveChart.select("a").on("click", to_js(partial(filter_all, [moveChart, volumeChart])))

numberFormat = ".2f"
dateFormatSpecifier = "%m/%d/%Y"
dateFormat = d3.timeFormat(dateFormatSpecifier)
data = pd.read_csv("./ndx.csv", parse_dates=["date"], date_format=dateFormatSpecifier)
data["day"] = data["date"].dt.strftime("%a")
data["month"] = data["date"].dt.to_period("M").dt.to_timestamp().dt.date
data["quarter"] = data["date"].dt.quarter.map("Q{:d}".format)
data["year"] = data["date"].dt.year
data["date"] = data["date"].dt.date


def default_converter(value, _ignored1, _ignored2):
    if isinstance(value, dt.date):
        return js.Date.new(value.year, value.month - 1, value.day)
    raise value


ndx = crossfilter(
    to_js(data.to_dict(orient="records"), default_converter=default_converter)
)
all = ndx.groupAll()

yearlyDimension = ndx.dimension("year")
yearlyPerformanceGroup = yearlyDimension.group().reduce(
    to_js(year_add), to_js(year_remove), to_js(year_initialize)
)

dateDimension = ndx.dimension("date")
moveMonths = ndx.dimension("month")
monthlyMoveGroup = moveMonths.group().reduceSum(to_js(lambda d: abs(d.close - d.open)))
volumeByMonthGroup = moveMonths.group().reduceSum(to_js(lambda d: d.volume / 500000))
indexAvgByMonthGroup = moveMonths.group().reduce(
    to_js(month_add), to_js(month_remove), to_js(month_initialize)
)

gainOrLoss = ndx.dimension(to_js(lambda d, *_: "Loss" if d.open > d.close else "Gain"))
gainOrLossGroup = gainOrLoss.group()
fluctuation = ndx.dimension(
    to_js(lambda d, *_: round((d.close - d.open) / d.open * 100))
)
fluctuationGroup = fluctuation.group()
quarter = ndx.dimension("quarter")
quarterGroup = quarter.group().reduceSum(to_js(lambda d: d.volume))
dayOfWeek = ndx.dimension("day")
dayOfWeekGroup = dayOfWeek.group()

(
    yearlyBubbleChart.width(990)
    .height(250)
    .transitionDuration(1500)
    .margins(to_js({"top": 10, "right": 50, "bottom": 30, "left": 40}))
    .dimension(yearlyDimension)
    .group(yearlyPerformanceGroup)
    .colors(d3.schemeRdYlGn[9])
    .colorDomain([-500, 500])
    .colorAccessor(to_js(lambda d, i: d.value["absGain"]))
    .keyAccessor(to_js(lambda d: d.value["absGain"]))
    .valueAccessor(to_js(lambda d: d.value["percentageGain"]))
    .radiusValueAccessor(to_js(lambda d: d.value["fluctuationPercentage"]))
    .maxBubbleRelativeSize(0.3)
    .x(d3.scaleLinear().domain([-2500, 2500]))
    .y(d3.scaleLinear().domain([-100, 100]))
    .r(d3.scaleLinear().domain([0, 4000]))
    .elasticY(True)
    .elasticX(True)
    .yAxisPadding(100)
    .xAxisPadding(500)
    .renderHorizontalGridLines(True)
    .renderVerticalGridLines(True)
    .xAxisLabel("Index Gain")
    .yAxisLabel("Index Gain %")
    .renderLabel(True)
    .label(to_js(lambda d: d.key))
    .renderTitle(True)
    .title(
        to_js(
            lambda p: "\n".join(
                [
                    str(p.key),
                    f"Index Gain: {p.value['absGain']:{numberFormat}}",
                    f"Index Gain in Percentage: {p.value['percentageGain']:{numberFormat}}%",
                    f"Fluctuation / Index Ratio: {p.value['fluctuationPercentage']:{numberFormat}}%",
                ]
            )
        )
    )
    .yAxis()
    .tickFormat(to_js(lambda v, *_: f"{v}%"))
)
(
    gainOrLossChart.width(180)
    .height(180)
    .radius(80)
    .dimension(gainOrLoss)
    .group(gainOrLossGroup)
    .label(to_js(gainOrLossLabel))
)
(
    quarterChart.width(180)
    .height(180)
    .radius(80)
    .innerRadius(30)
    .dimension(quarter)
    .group(quarterGroup)
)
(
    dayOfWeekChart.width(180)
    .height(180)
    .margins(to_js({"top": 20, "left": 10, "right": 10, "bottom": 20}))
    .group(dayOfWeekGroup)
    .dimension(dayOfWeek)
    .ordinalColors(["#3182bd", "#6baed6", "#9ecae1", "#c6dbef", "#dadaeb"])
    .label(to_js(lambda d: d.key))
    .title(to_js(lambda d, *_: d.value))
    .elasticX(True)
    .xAxis()
    .ticks(4)
)
(
    fluctuationChart.width(420)
    .height(180)
    .margins(to_js({"top": 10, "right": 50, "bottom": 30, "left": 40}))
    .dimension(fluctuation)
    .group(fluctuationGroup)
    .elasticY(True)
    .centerBar(True)
    .gap(1)
    .round(to_js(floor))
    .alwaysUseRounding(True)
    .x(d3.scaleLinear().domain([-25, 25]))
    .renderHorizontalGridLines(True)
    .filterPrinter(
        to_js(
            lambda filters: f"{filters[0][0]:{numberFormat}}% -> {filters[0][1]:{numberFormat}}%"
        )
    )
)
fluctuationChart.xAxis().tickFormat(to_js(lambda v, *_: f"{v}%"))
fluctuationChart.yAxis().ticks(5)
(
    moveChart.renderArea(True)
    .width(990)
    .height(200)
    .transitionDuration(1000)
    .margins(to_js({"top": 30, "right": 50, "bottom": 25, "left": 40}))
    .dimension(moveMonths)
    .mouseZoomable(True)
    .rangeChart(volumeChart)
    .x(
        d3.scaleTime().domain(
            to_js(
                [dt.date(1985, 1, 1), dt.date(2012, 12, 31)],
                default_converter=default_converter,
            )
        )
    )
    .round(d3.timeMonth.round)
    .xUnits(d3.timeMonths)
    .elasticY(True)
    .renderHorizontalGridLines(True)
    .legend(dc.legend().x(800).y(10).itemHeight(13).gap(5))
    .brushOn(False)
    .group(indexAvgByMonthGroup, "Monthly Index Average")
    .valueAccessor(to_js(lambda d, _: d.value["avg"]))
    .stack(monthlyMoveGroup, "Monthly Index Move", to_js(lambda d, _: d.value))
    .title(to_js(moveTitle))
)
(
    volumeChart.width(990)
    .height(40)
    .margins(to_js({"top": 0, "right": 50, "bottom": 20, "left": 40}))
    .dimension(moveMonths)
    .group(volumeByMonthGroup)
    .centerBar(True)
    .gap(1)
    .x(
        d3.scaleTime().domain(
            to_js(
                [dt.date(1985, 1, 1), dt.date(2012, 12, 31)],
                default_converter=default_converter,
            )
        )
    )
    .round(d3.timeMonth.round)
    .alwaysUseRounding(True)
    .xUnits(d3.timeMonths)
)
(
    nasdaqCount.crossfilter(ndx)
    .groupAll(all)
    .html(
        to_js(
            {
                "some": r"<strong>%filter-count</strong> selected out of <strong>%total-count</strong> records"
                + " | <a href='#'>Reset All</a>",
                "all": "All records selected. Please click on the graph to apply filters.",
            }
        )
    )
    .on(
        "renderlet",
        to_js(lambda chart: chart.select("a").on("click", to_js(reset_all))),
    )
)
(
    nasdaqTable.dimension(dateDimension)
    .section(to_js(lambda d, *_: f"{d.date.getFullYear()}/{d.date.getMonth() + 1:02d}"))
    .size(10)
    .columns(
        to_js(
            [
                {
                    "label": "Date",
                    "format": lambda d: dateFormat(d.date),
                },
                "open",
                {
                    "label": "Change",
                    "format": lambda d: f"{d.close - d.open:{numberFormat}}",
                },
                "volume",
            ]
        )
    )
    .sortBy(to_js(lambda d: d.date))
    .order(d3.ascending)
    .on(
        "renderlet",
        to_js(lambda table: table.selectAll(".dc-table-group").classed("info", True)),
    )
)
dc.renderAll()
