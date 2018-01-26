#!/bin/sh
#SBATCH --partition=general-compute
#SBATCH --time=00:15:00
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=IB&CPU-E5645
#SBATCH --job-name="mss_test"
#SBATCH --output=test-mpi-debug-%j.out
#SBATCH --error=test-mpi-debug-%j.err
#SBATCH --mail-user=amansuni@buffalo.edu
#SBATCH --mail-type=ALL


echo "SLURM_JOB_ID="$SLURM_JOB_ID
echo "SLURM_JOB_NODELIST="$SLURM_JOB_NODELIST
echo "SLURM_NNODES="$SLURM_NNODES
echo "SLURMTMPDIR="$SLURMTMPDIR
echo "working directory ="$SLURM_SUBMIT_DIR

echo "#####################################"
module load intel/17.0
module load intel-mpi/2017.0.1
module list
ulimit -s unlimited

#
NPROCS=`srun --nodes=${SLURM_NNODES} bash -c 'hostname' | wc -l`
echo NPROCS=$NPROCS


export I_MPI_DEBUG=4
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
srun ./mss 10000000

#
echo "All Done!"