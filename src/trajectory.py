import math

class Event:
    # def __init__(self):
        # self.x = 0
        # self.y = 0
        # self.z = 0
        # self.t = 0

    def __init__(self, x=0, y=0, z=0, t=0):
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        
    def __add__(self, other):
        new_state = Event()
        new_state.x = self.x + other.x
        new_state.y = self.y + other.y
        new_state.z = self.z + other.z
        new_state.t = self.t + other.t
        return new_state

    def __sub__(self, other):
        new_state = Event()
        new_state.x = self.x - other.x
        new_state.y = self.y - other.y
        new_state.z = self.z - other.z
        new_state.t = self.t - other.t
        return new_state

    def __mul__(self, coefficient):
        new_state = Event()
        new_state.x = self.x * coefficient
        new_state.y = self.y * coefficient
        new_state.z = self.z * coefficient
        new_state.t = self.t * coefficient
        return new_state

class Corner:
    def __init__(self, base, v0, v1):
        self.base = base
        self.v0 = v0
        self.v1 = v1

    def sample_weights(self, N, tau):
        beta = 2 - N
        alpha = 1 - beta

        return alpha * math.pow(tau, N) + beta * math.pow(tau, N+1)
        
    def sample_tau(self, tau):
        N = 3
        
        c0 = self.sample_weights(N, 1 - tau)
        c1 = self.sample_weights(N, tau)
                
        return self.base + self.v0 * c0 + self.v1 * c1

    def sample_time(self, time):
        tau_low = 0
        tau_high = 1
        
        for i in range(0, 10):
            current_tau = (tau_low + tau_high) / 2
            current_time = self.sample_tau(current_tau).t
            if current_time < time:
                tau_low = current_tau
            else:
                tau_high = current_tau

        return self.sample_tau((tau_low+tau_high)/2)
    
class Curve:
    def __init__(self):
        self.waypoints = []

    def sample_smooth (self, time):
        assert(time >= 0)
        assert(time < self.waypoints[ len(self.waypoints) - 1 ].t)

        n = -1
        
        for i in range(1, len(self.waypoints) - 1):
            t_low  = (self.waypoints[i-1].t + self.waypoints[i].t  ) / 2
            t_high = (self.waypoints[i].t   + self.waypoints[i+1].t) / 2
            if t_low <= time <= t_high:
                n = i

        assert(n != -1)

        base = self.waypoints[n]
        v0   = (self.waypoints[n-1] - base) * 0.5
        v1   = (self.waypoints[n+1] - base) * 0.5

        corner = Corner(base, v0, v1)
        result = corner.sample_time(time)
        
        # print("time: {}, result.t: {}".format(time, result.t))
        
        return result

        
    def sample_direct (self, time):
        assert(time >= 0)
        assert(time < self.waypoints[ len(self.waypoints) - 1 ].t)

        n = -1
        
        for i in range(0, len(self.waypoints) - 1):
            if self.waypoints[i].t <= time <= self.waypoints[i+1].t:
                n = i

        assert(n != -1)

        tau = (time - self.waypoints[n].t) / (self.waypoints[n+1].t - self.waypoints[n].t)
        result = self.waypoints[n] + (self.waypoints[n+1] - self.waypoints[n]) * tau

        # print("time: {}, result.t: {}".format(time, result.t))
        
        return result

