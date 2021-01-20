import numpy as np

def qr(A):
    """ Calculate the QR decomposition, preserving the directions of the
        columns.

        Inputs:
            A - A 2D numpy array

        Outputs:
            Q - A 2D numpy array of an orthogonal matrix
            R - A 2D numpy array of an upper triangular matrix

            The output arrays will have the property that A = QR.
    """
    Q, R = np.linalg.qr(A)
    signs = np.diag( (np.diag(R)>-1e-10)*2.0 - 1 )
    Q = Q @ signs
    R = signs @ R
    return Q, R

def VRdecomposition(A):
    """ Given a square orthogonal matrix A with determinant 1, decompose A into
        a series of rotations in mutually orthogonal 2D planes.

        Inputs:
            A - A 2D numpy array representing a square orthogonal matrix of
                determinant 1.

        Outputs:
            V - A 2D numpy array representing a square orthogonal matrix
            thetas - A 1D numpy array representing the rotations used

            The output arrays will have the property that A V[2j-1:2j,:] = 
            V[2j-1:2j,:] [ cos(thetas[j]), sin(thetas[j]); -sin(thetas[j]), 
            cos(thetas[j]) ] for all j from 1 to d, where A is a 2d by 2d array.

        Notes:
            The code assumes that A is randomly generated, and that A is of even
            dimension. This way, the chance that +1 or -1 is an eigenvalue is
            effectively zero. This needs to be fixed for future versions.
    """


    d = A.shape[0] // 2

    # Obtain the eigenvalues and eigenvectors, and sort by them in order of 
    # increasing real component for the eigenvalues.
    eigvals, eigvecs = np.linalg.eig(A)
    ind = np.argsort(eigvals, axis=0)
    eigvals = eigvals[ind]
    eigvecs = eigvecs[:,ind]
    
    # Find the columns of V, and the angles of rotation:
    V = np.zeros( A.shape )
    thetas = np.zeros( d )

    for i in range(d):

        eigenvalue = eigvals[2*i]
        
        V[:, 2*i  ] = np.real( eigvecs[:,2*i] )
        V[:, 2*i+1] = np.imag( eigvecs[:,2*i] )

        theta = np.arctan2(np.imag(eigenvalue), np.real(eigenvalue))
        thetas[i] = theta

    # Make the columns of V orthogonal to one another.
    V, _ = qr(V)

    return (V,thetas) 


def interpolateFrames(Fa, Fz):
    """ Given a source frame Fa and target frame Fz, calculate paramters used
        to create a continuous path of frames from Fa to Fz.

        Inputs:
            Fa - A 2D numpy array representing an orthogonal matrix of size 
                (p,d)
            Fz - A 2D numpy array representing an orthogonal matrix of size 
                (p,d)

        Outputs:
            B - A 2D numpy array representing an orthogonal matrix of size 
                (p,2d)
            thetas - A 1D numpy array representing angles in radians of size 
                (d)
            Wa - A 2D numpy array representing an orthogonal matrix of size
                (2d, d)

            The outputs will have the property that Fa = B Wa, and Fz = B R Wa
            where R is a block diagonal matrix of Givens rotations where 
            R[ 2j:2j+1, 2j:2j+1 ] = [cos(thetas[j]), sin(thetas[j]); 
            -sin(thetas[j]), cos(thetas[j])] for j from 1 to d.
    """

    d = Fa.shape[1]

    # Create B' to as a basis for the span of Wa' and Wz'. By construction, Wa'
    # is a diagonal matrix of all ones.
    B_prime, R = qr( np.concatenate( (Fa,Fz), axis=1 ) )
    Wa_prime = R[:, :d]
    Wz_prime = R[:, d:]
    
    
    # Create an orthogonal matrix A with determinant 1 where the first d columns
    # match with Wz'.
    A = np.random.normal(size=(2*d,2*d))
    A[:,:d] = Wz_prime
    A, _ = qr(A)
    if np.linalg.det(A) < 0: A[:,-1] *= -1
    
    # Decompose A into V R(thetas) V^T, and let B = B' V and Wa = V^T Wa'. That
    # way, Fa = B Wa and Fz = B R(thetas) Wa.
    V, thetas = VRdecomposition(A)
    B = B_prime @ V
    Wa = np.transpose(V) @ Wa_prime


    return B, thetas, Wa

def constructR(thetas, oddDimension=False):
    """ Given a list of angles, reconstruct a block diagonal matrix consisting
        of Givens rotations with the angles specified by the thetas.

        Inputs:
            thetas - A 1D numpy array representing angles in radians of size 
                (d)

        Outputs:
            R - A 2D numpy array representing an block diagonal matrix of size
                (2d,2d)

            The output has the property that: R[ 2j:2j+1, 2j:2j+1 ] = 
            [cos(thetas[j]), sin(thetas[j]); -sin(thetas[j]), cos(thetas[j])] 
            for j from 1 to d.
    """
    d = np.shape(thetas)[0]
    m = 2*d + int(oddDimension)
    
    R = np.zeros( (m, m) )

    for i in range(d):
        theta = thetas[i]
        R[2*i  , 2*i  ] =   np.cos(theta)
        R[2*i  , 2*i+1] =   np.sin(theta)
        R[2*i+1, 2*i  ] = - np.sin(theta)
        R[2*i+1, 2*i+1] =   np.cos(theta)
        
    if oddDimension:
        R[2*d, 2*d] = 1
    

    return R