import random, math

#-constants-----------------------------------------------------------------------
GRAVITY = -100
EXPL_VEL_M, EXPL_VEL_V = 40, 40
EXPL_SHAPE = 0.75
EXPL_SHAPE_V = 50
EXPL_R_MIN, EXPL_R_MAX = math.pi/4, 3*math.pi/4

TWO_PI = math.pi * 2

#-class-definitions---------------------------------------------------------------
class ParticleSystem:
    def __init__(self, position, startColor, endColor, lifespan=3):
        # define system properties
        self.pos = position

        self.col = startColor
        self.colS, self.colF = startColor, endColor

        self.children = []
        self.canSpawn = True

        self.age = 0
        self.lifespan = lifespan
        self.alive = True

    def update(self, dt):
        # print(self.age, self.lifespan, self.pos, self.col, self.canSpawn, len(self.children))
        self.age += dt
        # update children
        for index, child in reversed(list(enumerate(self.children))):
            child.update(dt)
            if not child.alive:
                del self.children[index]
        # spawn children
        if self.canSpawn: self.spawn()
        # update color
        self.col = colorInterp(self.colS, self.colF, self.age, self.lifespan)
        # kill if too old
        self.alive = self.age < self.lifespan

    def spawn(self):
        for ii in range(300):
            pow, rad = EXPL_VEL_M+random.uniform(-EXPL_VEL_V, EXPL_VEL_V), random.uniform(EXPL_R_MIN, EXPL_R_MAX)
            self.children.append( Particle(self.pos.copy(),[(pow*2*(1-EXPL_SHAPE))*math.cos(rad), (pow*2*EXPL_SHAPE)*math.sin(rad), 0], [0, GRAVITY, 0], self.col.copy(), self.colF) )
        self.canSpawn = False

class Particle:
    def __init__(self, position, velocity, acceleration, startColor, endColor, lifespan = 1.5):
        # define particle properties
        self.pos = position
        self.vel = velocity
        self.acc = acceleration

        self.col = startColor
        self.colS, self.colF = startColor, endColor

        self.age = 0
        self.lifespan = lifespan
        self.alive = True

    def update(self, dt):
        self.age += dt
        # update velocities
        self.vel[0] += self.acc[0] * dt
        self.vel[1] += self.acc[1] * dt
        self.vel[2] += self.acc[2] * dt
        # update velocities
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.pos[2] += self.vel[2] * dt
        # update color
        self.col = colorInterp(self.colS, self.colF, self.age, self.lifespan)
        # kill if too old
        self.alive = self.age < self.lifespan

#-helper/utility-functions--------------------------------------------------------
# COLOR INTERPOLATION
#   interpolated between the intial and final colors as RGB(A?)
#   age is the current age of the particle in frames
#   particle lifespan as the dying age of the particle in frames
#   (lifespan could be optional (=1) if age is a fraction 0.0->1.0)
def colorInterp(initial, final, age, particleLifespan = 1):
    frac = age/particleLifespan
    newR = initial[0] + frac*(final[0]-initial[0])
    newG = initial[1] + frac*(final[1]-initial[1])
    newB = initial[2] + frac*(final[2]-initial[2])
    newA = initial[3] + frac*(final[3]-initial[3])
    return [newR, newG, newB, newA]
