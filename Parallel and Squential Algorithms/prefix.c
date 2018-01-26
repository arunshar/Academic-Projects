#include <stdio.h>
#include "mpi.h"
#include <stdlib.h>
#include <time.h>

long *create_random_ints(long num_elements){
	long *random_ints = malloc(num_elements * sizeof(long));
	int i;
	for(i = 0; i < num_elements; i++) {
		random_ints[i] = rand() % 100000000 + (-50000000);
	}
	return random_ints;
}


int main(argc, argv)
	int argc;
	char **argv;
{
	if(argc !=2) {
		fprintf(stderr,"usage ");
		exit(1);
	}
	struct timeval st,et;
	clock_t tic,tock;
	int rank,size;
	int len;
	long element_count = atol(argv[1]);
	srand(time(NULL));
	char procname[MPI_MAX_PROCESSOR_NAME];
        MPI_Init( &argc, &argv );
        MPI_Comm_size( MPI_COMM_WORLD, &size );
        MPI_Comm_rank( MPI_COMM_WORLD,  &rank );
        MPI_Get_processor_name(procname,&len);
	int j;	
	long *receiveBuff = NULL;	
	if (rank == 0) {
		receiveBuff = malloc(element_count * sizeof(long));
	}
	
	int sub_element_size = element_count / size;
	long *sub_random_elements = malloc(sub_element_size * sizeof(long));

	
	sub_random_elements = create_random_ints(sub_element_size);
	/*for (j = 0; j< sub_element_size; j ++) {
		printf("Item is %d in %d\n", sub_random_elements[j],rank);
	}*/
	
	tic = clock();
	gettimeofday(&st,NULL);
	
	MPI_Gather(sub_random_elements, sub_element_size, MPI_LONG, receiveBuff, sub_element_size, MPI_LONG, 0, MPI_COMM_WORLD);
	
 		
	/*MPI_Scatter(random_ints,sub_element_size, MPI_INT,sub_random_elements,sub_element_size,MPI_INT,0,MPI_COMM_WORLD); */
	
	long *prefixSum = malloc(sub_element_size * sizeof(long));
	prefixSum[0] = sub_random_elements[0];

	for (j = 1; j < sub_element_size; j++) {
		prefixSum[j] = prefixSum[j-1] + sub_random_elements[j];
	}

	long sumToSend;
	
	if ( rank != 0 ) {
		MPI_Recv(&sumToSend,1,MPI_LONG, rank - 1,2,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
		/*printf("Received %d from %d \n",sumToSend,(rank-1));*/
		for(j=0; j< sub_element_size; j++) {
			prefixSum[j] = prefixSum[j] + sumToSend;
		}
		if (rank <= size-2) {
			sumToSend = prefixSum[sub_element_size -1];
			MPI_Send(&sumToSend,1,MPI_LONG,rank + 1,2,MPI_COMM_WORLD);
			/*printf("Sent %d to %d\n",sumToSend,rank+1);*/
		} 
	} 
	else {
		sumToSend = prefixSum[sub_element_size - 1];
		MPI_Send(&sumToSend,1,MPI_LONG,rank + 1,2,MPI_COMM_WORLD);
		/*printf("Sent %d to %d \n",sumToSend,rank+1);*/
	}	
        
	/*for(j = 0; j < sub_element_size; j++) {
        	printf("Prefix Sum ---> element is %d at %d of process %d\n",prefixSum[j],j,rank);
        }*/

	long *maxArray = malloc(sub_element_size * sizeof(long));
	j = sub_element_size - 1;
	long maxToTransfer;
	long maxPositionArray[2];
	long finalMaxPosition;
	
	if(rank == size - 1) {
		int counter = 1;
		maxPositionArray[0] = rank;
		maxArray[sub_element_size -1] = prefixSum[sub_element_size -1];
		maxPositionArray[1] = sub_element_size - 1;
		for(j = sub_element_size - 2; j >= 0; j--) {
			if (prefixSum[j] > maxArray[j+1]) {
				maxArray[j] = prefixSum[j];
				maxPositionArray[1] = j;
				counter++;
			}
			else {
				maxArray[j] = maxArray[j + 1];
				counter++;
			}
		}
		
		/*for( j =0; j < sub_element_size; j++){
			printf(" Max element -> %d at position %d from process %d \n",maxArray[j],j,rank); 
		}*/
		maxToTransfer = maxArray[0];
		MPI_Send(&maxToTransfer,1,MPI_LONG, (rank - 1), 0, MPI_COMM_WORLD);
		MPI_Send(maxPositionArray,2,MPI_LONG,(rank - 1),1,MPI_COMM_WORLD);
	}
	else {
		int counter = 0;
		MPI_Recv(&maxToTransfer,1,MPI_LONG,(rank + 1),0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
		printf("Max Received %d in process %d \n",maxToTransfer,rank);
		MPI_Recv(maxPositionArray,2,MPI_LONG,(rank + 1),1,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
		printf("Max start position is %d in processor %d \n",maxPositionArray[1],maxPositionArray[0]);

		if (prefixSum[sub_element_size -1] > maxToTransfer) {
			maxArray[sub_element_size -1] = prefixSum[sub_element_size -1];
			maxPositionArray[1] = sub_element_size - 1;
			maxPositionArray[0] = rank;
		}
		else {
			maxArray[sub_element_size -1] = maxToTransfer;
		}

		printf("checkpoint 1 from %d\n",rank);

		for(j = sub_element_size -2; j >= 0 ; j--) {
			if(prefixSum[j] > maxArray[j+1]) {
				maxArray[j] = prefixSum[j];
				maxPositionArray[1] = j;
				maxPositionArray[0] = rank;
				counter++;
			}
			else {
				maxArray[j] = maxArray[j + 1];
				counter++;
			}
		}
		printf(" count is %d for %d after cp1\n",counter,rank);

		/*for (j= 0; j < sub_element_size; j ++) {
			printf("Max element -> %d at position %d from process %d \n",maxArray[j],j,rank);
		} */
		printf("checkpoint 2 from %d\n",rank);
		maxToTransfer = maxArray[0];
		if( (rank -1) != -1) {
			MPI_Send(&maxToTransfer,1,MPI_2INT,(rank -1),0,MPI_COMM_WORLD);
			MPI_Send(maxPositionArray,2,MPI_2INT,(rank -1),1,MPI_COMM_WORLD);
		} 
		if (rank == 0) {
			finalMaxPosition = (maxPositionArray[0] * sub_element_size) + maxPositionArray[1];
			printf("final max at position %d in processor %d\n",finalMaxPosition,maxPositionArray[0]);
		}

	}
	printf("Checkpoint 3 from %d\n",rank);
	long localForm[sub_element_size];
		
        for(j=0; j< sub_element_size; j++) {
                localForm[j] = maxArray[j] - prefixSum[j] + sub_random_elements[j];
                /*printf("%d = %d - %d + %d \n",localForm[j],maxArray[j],prefixSum[j],sub_random_elements[j]);*/
        }
	printf("checkpoint 4\n");
	struct {
		int value;
		int index;
	} in,out;

	in.value = localForm[0];
	in.index = 0;
	
	for(j = 1; j < sub_element_size; j++) {
		if ( in.value < localForm[j]) {
			in.value = localForm[j];
			in.index = j;
		}
	}
	printf("checkpoint 5\n");

	in.index = rank * sub_element_size + in.index;
	MPI_Reduce (&in, &out, 1, MPI_2INT, MPI_MAXLOC, 0, MPI_COMM_WORLD);
	printf("checkpoint 6\n");
	long maxRank,maxVal,maxIndex;
	if ( rank == 0 ) {
		maxVal = out.value;
		maxRank = out.index / sub_element_size;
		maxIndex = out.index % element_count;
		
		printf("Global max is %d on process %d at index %d \n" , maxVal,maxRank,maxIndex);
		/*printf(" Max seq is \n");
		for(j = maxIndex;j <= finalMaxPosition;j++) {
			printf("%d ",receiveBuff[j]);
		}
		printf("\n");*/
                tock = clock();
		gettimeofday(&et,NULL);
                printf("Elapsed time to compute max subsequence of %d data items is : %lf seconds \n", element_count, (double)(tock - tic) / CLOCKS_PER_SEC);
		printf("time in ms : %lu\n", et.tv_usec - st.tv_usec);
		printf("checkpoint 7\n");

	}
	
        MPI_Finalize();
        return 0;
}
