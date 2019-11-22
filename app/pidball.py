from .tools import interval
#import numpy as np

class PIDBall():
    def __init__(self, input_params):
        params = {'s_0':10, 'sp':5, 'v_0':0, 'dt':0.01, 't_f':1, 'k_p': 1500, 'k_i': 300, 'k_d': 50}
        params.update(input_params)
        self.params = params

        self.reset()

    def reset(self):
        self.s_0 = self.params['s_0']
        self.s_last = self.s_0
        self.s_sp = self.params['sp']

        self.v_0 = self.params['v_0']

        self.t_0 = 0
        self.t_f = self.params['t_f']
        self.dt = self.params['dt']

        self.k_p = self.params['k_p']
        self.k_i = self.params['k_i']
        self.k_d = self.params['k_d']

        self.g = -9.8

        self.t_array = [self.t_0]
        self.s_array = [self.s_0]
        self.integral = 0

    def data(self):
        return [self.t_array, self.s_array]

    def push_data(self, t, s):
        self.t_array.append(t)
        self.s_array.append(s)

    def delta_s(self):
        return self.s_array[-1] - self.s_array[-2]

    def s_t(self, s, v):
        self.s_last = s
        s += v * self.dt
        return s

    def v_t(self):
        return self.delta_s()/self.dt if len(self.s_array) > 1 else self.v_0

    def pid(self, sense, set_point):
        kp, ki, kd = self.k_p, self.k_i, self.k_d
        dt = self.dt
        sense_l = self.s_last

        e = set_point - sense
        e_l = set_point - sense_l

        # Integral calculation
        self.integral += dt*(e+e_l)/2
        int_e = self.integral
        # If you preffer numpy, change above towo lines with:
        # int_e = np.trapz(e, dx=dt)

        # Derivative calculation
        de_dt = (e-e_l)/dt

        # PID
        p = kp * e
        i = ki * int_e
        d = kd * de_dt

        return p+i+d

    def run(self):
        self.reset()

        t_0 = self.t_0
        t_f = self.t_f
        dt = self.dt
        period = interval(t_0, t_f, dt)

        s_t = self.s_t
        set_point = self.s_sp
        v_t = self.v_t
        pid = self.pid
        g = self.g

        s = self.s_0
        for t in period:
            control = pid(s, set_point)
            a = g + control
            v = v_t() + a*dt
            s = s_t(s, v)
            self.push_data(t, s)

        return self.data()
