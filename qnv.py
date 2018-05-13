import numpy as np
import math

def quatInv(q1): #to get inverse of a quaternion
	qi = np.zeros(4)
	qi[0] = q1[0]
	qi[1:4] = -1*q1[1:4].copy()
	return qi

<<<<<<< HEAD

def quatMultiply(q1,q2):
	#quaternion is scalar, vector. function multiplies 2 quaternions
=======
def quatMultiplynorm(q1,q2): #returns quaternion product (product is a unit quaternion)
>>>>>>> 6750e09555eb2dff9eac0b318fd627503d713511

	a1 = q1[0:1].copy()
	a2 = q2[0:1].copy()
	
	b1 = (q1[1:4].copy())
	b2 = (q2[1:4].copy())
	
	a = a1*a2 - np.dot(b1,b2)
	b = a1*b2 + a2*b1 + np.cross(b1,b2)
	q = np.hstack((a,b))
	
	#q = q/np.linalg.norm(q)
	return q

def quatMultiplyUnnorm(q1,q2): #returns quaternion product (product is not a unit quaternion)

	a1 = q1[0:1].copy()
	a2 = q2[0:1].copy()
	
<<<<<<< HEAD
	#rotates vecctor x by quaternion q
	#M = np.array([[q[0]**2 + q[1]**2 - q[2]**2 - q[3]**2,2*]])
	if 	np.array_equal(x,np.array([0,0,0])):
		x2 = np.array([0.,0.,0.])
	else:
		qi = np.zeros(4)
		qi[0] = q[0].copy()
		qi[1:4] = -1*q[1:4].copy()
		y = np.hstack(([0.],x.copy()))
		y = quatMultiply(q,y)
		y = quatMultiply(y,qi)

		x2 = y[1:4]	
	
	return x2

def quatDer1(q,w): #if w is in body frame, q takes from body to inertial
=======
	b1 = (q1[1:4].copy())
	b2 = (q2[1:4].copy())
	
	a = a1*a2 - np.dot(b1,b2)
	b = a1*b2 + a2*b1 + np.cross(b1,b2)
	q = np.hstack((a,b))
	return q

def quatRotate(q,x): #rotates vecctor x by quaternion q
	
	if np.count_nonzero(x) == 0:
		return x
	qi = quatInv(q)
	y = np.hstack(([0.],x.copy()))
	y = quatMultiplyUnnorm(q,y)
	y = quatMultiplyUnnorm(y,qi)
	x2 = y[1:4]
	return x2

def quatDer1(q,w): # w is angular velocity of body wrt inertial frame in body frame. q transforms inertial frame vector to body frame
>>>>>>> 6750e09555eb2dff9eac0b318fd627503d713511
	W = np.array([[0,-w[0],-w[1],-w[2]],[w[0],0,w[2],-w[1]],[w[1],-w[2],0,w[0]],[w[2],w[1],-w[0],0]])
	q_dot = 0.5*np.dot(W,q)

	return q_dot
'''
def quatDer2(q,w): #if w is in inertial frame, q takes from body to inertial
	W = np.array([[0,-w[0],-w[1],-w[2]],[w[0],0,-w[2],w[1]],[w[1],w[2],0,-w[0]],[w[2],-w[1],w[0],0]])
	q_dot = 0.5*np.dot(W,q)

	return q_dot
'''
def rotm2quat(A): #returns a quaternion whose scalar part is positive to keep angle between -180 to +180 deg.

	q0 = 1 + np.trace(A)
	q1 = 1 + A[0,0] - A[1,1] - A[2,2]
	q2 = 1 - A[0,0] + A[1,1] - A[2,2]
	q3 = 1 - A[0,0] - A[1,1] + A[2,2]
	qm = max(q0,q1,q2,q3)
	if(qm==q0):
		q0 = math.sqrt(q0)/2
		q1 = (A[1,2] - A[2,1])/(4*q0)
		q2 = (A[2,0] - A[0,2])/(4*q0)
		q3 = (A[0,1] - A[1,0])/(4*q0)

	elif(qm==q1):
		q1 = math.sqrt(q1)/2
		q0 = (A[1,2] - A[2,1])/(4*q1)
		q2 = (A[0,1] + A[1,0])/(4*q1)
		q3 = (A[0,2] + A[2,0])/(4*q1)

	elif(qm==q2):
		q2 = math.sqrt(q2)/2
		q0 = (A[2,0] - A[0,2])/(4*q2)
		q1 = (A[0,1] + A[1,0])/(4*q2)
		q3 = (A[1,2] + A[2,1])/(4*q2)

	else: 
		q3 = math.sqrt(q3)/2
		q0 = (A[0,1] - A[1,0])/(4*q3)
		q1 = (A[0,2] + A[2,0])/(4*q3)
		q2 = (A[1,2] + A[2,1])/(4*q3)

	q = np.array([q0,q1,q2,q3])
	q = q/np.linalg.norm(q)
	
	return q

def quat2rotm(q): #given a quaternion it returns a rotation matrix
	q1 = q[1]
	q2 = q[2]
	q3 = q[3]
	q0 = q[0]

	M1 = 2* np.array([[-q2**2 - q3**2,q1*q2,q1*q3],[q1*q2,-q1**2 - q3**2,q2*q3],[q1*q3,q2*q3,-q1**2-q2**2]])
	M2 = -2*q0*np.array([[0,-q3,q2],[q3,0,-q1],[-q2,q1,0]])
	M3 = np.identity(3)
	return M1 + M2 + M3

'''
def skew(v):
	return np.array([[0,-v[2],v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])

def theta2J(t):
	t1 = t[0]
	t2 = t[1]
	t3 = t[2]
	t4 = t[3]
	t5 = t[4]
	t6 = t[5]
	return np.array([[t1,t2,t3],[t2,t4,t5],[t3,t5,t6]])
'''
