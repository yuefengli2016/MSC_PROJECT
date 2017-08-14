# The MIT License (MIT)
# Copyright (c) 2014-2017 University of Bristol
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import division
from hyperstream import Tool, StreamInstance
import numpy as np

def perceptron_predictAndUpdate(x, w, y):
    errors = []
    results = []
    unit_step = lambda x: 0 if x < 0 else 1
    for i in range(len(x)-1):
        z = x[i]
	result = np.dot(w,z.T)
	error = y[i] - unit_step(result)
        errors.append(error)
	results.append(result)
        w += error * z
    count = 0
    for error in errors:
	if error == 0:
	    count += 1
    accurate = count/len(x)
    print (accurate)
    return w

def test(x, w, y):
    errors = []
    unit_step = lambda x: 0 if x < 0 else 1
    for i in range(len(x)-1):
	z = x[i]
	result = np.dot(w,z.T)
	error = y[i] - unit_step(result)
	errors.append(error)
    count = 0
    for error in errors:
	if error == 0:
	    count += 1
    accurate = count/len(x)
    return accurate
def read_csv_file():
    #timestamp = np.loadtxt("sonar_test.csv", delimiter=',', usecols=[0])
    x = np.loadtxt("sonar_all_data.csv", delimiter=',', usecols=range(1, 61))
    y = np.loadtxt("sonar_all_data.csv", delimiter=',', usecols=[61])
    return x, y


class Perceptron(Tool):
    """
    """

    def __init__(self):
        super(Perceptron, self).__init__()

    def _execute(self, sources, alignment_stream, interval):
        data = sources[0].window(interval, force_calculation=True)

        for timestamp, value in data:
            y_est = perceptron_predict(np.array(value["x"]), self.weights)
            self.weights = perceptron_update(np.array(value["x"]), self.weights, value["y"])
            yield StreamInstance(timestamp, y_est)

def main():
    x, y = read_csv_file()
    w = np.random.rand(len(x[1]))
    #w = [0]*len(x[1])
    print (w)
    w = perceptron_predictAndUpdate(x, w, y)
    print (w)
    a = test(x, w, y)
    print (a) 


if __name__ == '__main__':
   main()
