/* exp-random.c */

/* Instead of using a uniform distribution for process arrival
 * times, we'll use an exponential distribution, which should
 * better model the real-world system
 *
 * Poisson process
 *
 * M/M/1 queue
 *
 * Randomly generated values are the times between process arrivals
 *  (interarrival times)
 *
 * Events occur continuously and independently, but we have
 *  arrivals occurring at a constant average rate
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <time.h>

int main( int argc, char* argv[]) {
  int seed = argv[1];
  double lambda = argv[2];
  int upper_bound = argv[3];
  int stimulations = argv[4];
  int context_switch = argv[5];
  

  srand48( 64 );

  for ( int i = 0 ; i < iterations ; i++ ) {
    double lambda = 0.001;  /* average should be 1/lambda ==> 1000 */

    double r = drand48();   /* uniform dist [0.00,1.00) -- also check out random() */
    double x = -log( r ) / lambda;  /* log() is natural log */

    /* avoid values that are far down the "long tail" of the distribution */
    if ( x > 4096 ) { i--; continue; }

    printf( "r is %lf\n", r);
    printf( "x is %lf\n\n", x );

    sum += x;
    if ( i == 0 || x < min ) { min = x; }
    if ( i == 0 || x > max ) { max = x; }
  }

}
