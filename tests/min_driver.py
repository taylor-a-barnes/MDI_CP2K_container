import mdi
import sys

iarg = 1
while iarg < len(sys.argv):
    arg = sys.argv[iarg]

    if arg == "-mdi":
        # Initialize MDI
        if len(sys.argv) <= iarg+1:
            raise Exception("Argument to -mdi option not found")
        mdi.MDI_Init(sys.argv[iarg+1], None)
        iarg += 1
    else:
        raise Exception("Unrecognized argument")

    iarg += 1

# Connect to the engine
comm = mdi.MDI_Accept_Communicator()

# Get the name of the engine, which will be checked and verified at the end
mdi.MDI_Send_Command("<NAME", comm)
engine_name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)
print("Engine name: " + str(engine_name))

mdi.MDI_Send_Command("<NATOMS", comm)
natoms = mdi.MDI_Recv(1, mdi.MDI_INT, comm)
print("Number of atoms: " + str(natoms))

mdi.MDI_Send_Command("<NPARTICLES", comm)
nparticles = mdi.MDI_Recv(1, mdi.MDI_INT, comm)
print("Number of particles: " + str(nparticles))

mdi.MDI_Send_Command("<ENERGY", comm)
energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
print("Energy: " + str(energy))

mdi.MDI_Send_Command("<FORCES", comm)
forces = mdi.MDI_Recv(3*natoms, mdi.MDI_DOUBLE, comm)
#print("Forces: " + str(forces))

mdi.MDI_Send_Command("<COORDS", comm)
coords = mdi.MDI_Recv(3*natoms, mdi.MDI_DOUBLE, comm)

coords[1] += 0.1
mdi.MDI_Send_Command(">COORDS", comm)
mdi.MDI_Send(coords, 3*natoms, mdi.MDI_DOUBLE, comm)

mdi.MDI_Send_Command("<ENERGY", comm)
energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
print("Energy: " + str(energy))

#for i in range(10):
#    mdi.MDI_Send_Command("<ENERGY", comm)
#    energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
#    print("Energy: " + str(energy))

#mdi.MDI_Send_Command("<PE", comm)
#pe = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
#print("PE: " + str(pe))

#mdi.MDI_Send_Command("<KE", comm)
#ke = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
#print("KE: " + str(ke))

mdi.MDI_Send_Command("EXIT", comm)
