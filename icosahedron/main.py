from pyscript.ffi import to_js
from pyscript.js_modules import THREE
from pyscript import when, window, document
from js import Math, performance
import asyncio

mouse = THREE.Vector2.new()

renderer = THREE.WebGLRenderer.new({"antialias": True})
renderer.setSize(1000, 1000)
renderer.shadowMap.enabled = False
renderer.shadowMap.type = THREE.PCFSoftShadowMap
renderer.shadowMap.needsUpdate = True

document.body.appendChild(renderer.domElement)

@when("mousemove", "body")
def onMouseMove(event):
    event.preventDefault()
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1

camera = THREE.PerspectiveCamera.new(35, window.innerWidth / window.innerHeight, 1, 500)
scene = THREE.Scene.new()
cameraRange = 3

camera.aspect = window.innerWidth / window.innerHeight
camera.updateProjectionMatrix()
renderer.setSize( window.innerWidth, window.innerHeight )

setcolor = "#000000"

scene.background = THREE.Color.new(setcolor)
scene.fog = THREE.Fog.new(setcolor, 2.5, 3.5)

sceneGroup = THREE.Object3D.new()
particularGroup = THREE.Object3D.new()

def mathRandom(num = 1):
    setNumber = - Math.random() * num + Math.random() * num
    return setNumber

particularGroup =  THREE.Object3D.new()
modularGroup =  THREE.Object3D.new()

perms = to_js({"flatShading":True, "color":"#111111", "transparent":False, "opacity":1, "wireframe":False})

particle_perms = to_js({"color":"#FFFFFF", "side":THREE.DoubleSide})

def create_cubes(mathRandom, modularGroup):
    i = 0
    while i < 30:
        geometry = THREE.IcosahedronGeometry.new()
        material = THREE.MeshStandardMaterial.new(perms)
        cube = THREE.Mesh.new(geometry, material)
        cube.speedRotation = Math.random() * 0.1
        cube.positionX = mathRandom()
        cube.positionY = mathRandom()
        cube.positionZ = mathRandom()
        cube.castShadow = True
        cube.receiveShadow = True
        newScaleValue = mathRandom(0.3)
        cube.scale.set(newScaleValue,newScaleValue,newScaleValue)
        cube.rotation.x = mathRandom(180 * Math.PI / 180)
        cube.rotation.y = mathRandom(180 * Math.PI / 180)
        cube.rotation.z = mathRandom(180 * Math.PI / 180)
        cube.position.set(cube.positionX, cube.positionY, cube.positionZ)
        modularGroup.add(cube)
        i += 1

create_cubes(mathRandom, modularGroup)


def generateParticle(mathRandom, particularGroup, num, amp = 2):
    gmaterial = THREE.MeshPhysicalMaterial.new(particle_perms)
    gparticular = THREE.CircleGeometry.new(0.2,5)
    i = 0
    while i < num:
        pscale = 0.001+Math.abs(mathRandom(0.03))
        particular = THREE.Mesh.new(gparticular, gmaterial)
        particular.position.set(mathRandom(amp),mathRandom(amp),mathRandom(amp))
        particular.rotation.set(mathRandom(),mathRandom(),mathRandom())
        particular.scale.set(pscale,pscale,pscale)
        particular.speedValue = mathRandom(1)
        particularGroup.add(particular)
        i += 1

generateParticle(mathRandom, particularGroup, 200, 2)

sceneGroup.add(particularGroup)
scene.add(modularGroup)
scene.add(sceneGroup)

camera.position.set(0, 0, cameraRange)
cameraValue = False

ambientLight = THREE.AmbientLight.new(0xFFFFFF, 0.1)

light = THREE.SpotLight.new(0xFFFFFF, 3)
light.position.set(5, 5, 2)
light.castShadow = True
light.shadow.mapSize.width = 10000
light.shadow.mapSize.height = light.shadow.mapSize.width
light.penumbra = 0.5

lightBack = THREE.PointLight.new(0x0FFFFF, 1)
lightBack.position.set(0, -3, -1)

scene.add(sceneGroup)
#scene.add(light)
#scene.add(lightBack)
#scene.add(ambientLight)

rectSize = 3
intensity = 44
rectLight = THREE.RectAreaLight.new( 0x0FFFFF, intensity,  rectSize, rectSize )
rectLight.position.set( 0, 0, 1 )
rectLight.lookAt( 0, 0, 0 )
scene.add(rectLight)

raycaster = THREE.Raycaster.new()
uSpeed = 0.1

time = 0.0003
camera.lookAt(scene.position)

async def main():
    while True:
        time = performance.now() * 0.0003
        i = 0
        while i < particularGroup.children.length:
            newObject = particularGroup.children[i]
            newObject.rotation.x += newObject.speedValue/10
            newObject.rotation.y += newObject.speedValue/10
            newObject.rotation.z += newObject.speedValue/10
            i += 1

        i = 0
        while i < modularGroup.children.length:
            newCubes = modularGroup.children[i]
            newCubes.rotation.x += 0.008
            newCubes.rotation.y += 0.005
            newCubes.rotation.z += 0.003

            newCubes.position.x = Math.sin(time * newCubes.positionZ) * newCubes.positionY
            newCubes.position.y = Math.cos(time * newCubes.positionX) * newCubes.positionZ
            newCubes.position.z = Math.sin(time * newCubes.positionY) * newCubes.positionX
            i += 1

        particularGroup.rotation.y += 0.005

        modularGroup.rotation.y -= ((mouse.x * 4) + modularGroup.rotation.y) * uSpeed
        modularGroup.rotation.x -= ((-mouse.y * 4) + modularGroup.rotation.x) * uSpeed

        renderer.render( scene, camera )
        await asyncio.sleep(0.02)

main()