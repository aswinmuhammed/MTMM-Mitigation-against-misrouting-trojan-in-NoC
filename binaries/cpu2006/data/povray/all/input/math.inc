//    Persistence of Vision Ray Tracer version 3.5 Include File
//    File: math.inc
//    Last updated: 2002.04.29
//    Description: This file contains various math macros and functions

#ifndef(MATH_INC_TEMP)
#declare MATH_INC_TEMP = version;
#version 3.5;

#ifdef(View_POV_Include_Stack)
   #debug "including math.inc\n"
#end

#include "data/all/input/functions.inc"

// --------------------------------------------------------
// Statistics macros: (some from variate.inc)
// --------------------------------------------------------

// Mean(rewritten, original from basemcr.inc by Margus Ramst)
#macro Mean(A)
   #local N = dimension_size(A,1);
   #local C = 0;
//    (
//    #while(C<N-1)
//        A[C]+
//        #local C=C+1;
//    #end
//    A[C])/N
   #local V = 0;
   #while(C < N)
      #local V = V + A[C];
      #local C=C+1;
   #end
   (V/N)
#end

// Standard deviation(rewritten, original from basemcr.inc by Margus Ramst)
#macro Std_Dev(A, M)
   #local N = dimension_size(A,1);
   #local C = 0;
//    sqrt((
//    #while(C<N-1)
//        pow(A[C]-M,2)+
//        #local C=C+1;
//    #end
//    pow(A[C]-M,2))/N)
   #local V = 0;
   #while(C < N)
      #local V = V + pow(A[C] - M, 2);
      #local C=C+1;
   #end
   sqrt(V/N)
#end

// Macros for statistical analysis
// Input: an array of values
// Output: a global array "StatisticsArray" is
//         declared containing: N, Mean, Min, Max, StdDev
#macro GetStats(ValArr)
   #local SquareSum=0; #local Sum=0;
   #local Min=10e15;   #local Max=-10e15;
   #local N=dimension_size(ValArr,1);
   #local I=0;
   #while (I<N)
      #local Val=ValArr[I];
      #local Sum=Sum+Val;
      #local SquareSum=SquareSum+(Val*Val);
      #if (Val>Max)
         #local Max=Val;
      #end
      #if (Val<Min)
         #local Min=Val;
      #end
      #local I=I+1;
   #end
   #local Avg=Sum/N;
   #local StdDev=sqrt((SquareSum/N)-Avg*Avg);
   #debug concat("\nN      = ",str(N,0,0),"\n")
   #debug concat("Mean   = ",str(Avg,0,-1),"\n")
   #debug concat("Min    = ",str(Min,0,-1),"\n")
   #debug concat("Max    = ",str(Max,0,-1),"\n")
   #debug concat("StdDev = ",str(StdDev,0,-1),"\n")
   #declare StatisticsArray=array[5]{N,Avg,Min,Max,StdDev}
#end

// Input: an array with values and the wanted amount of intervals / bins.
// Output: a global array "HistogramArray" is declared,
//         it is a two dimensional array, the first value is the center
//         of the interval / bin, the second the amount of values
//         in that interval.
#macro Histogram(ValArr, Intervals)
   GetStats(ValArr)
   #local Min=StatisticsArray[2];
   #local Max=StatisticsArray[3];

   #local Intervals=int(Intervals);
   #local Width=(Max-Min)/(Intervals);

   #local HistArr=array[Intervals][2]
   #local I=0;
   #while(I<Intervals)
      #local HistArr[I][0]=Min+Width*(I+0.5);  // center of interval
      #local HistArr[I][1]=0;
      #local I=I+1;
   #end

   #local I=0;
   #while (I<N)                                // 'put' the values into the right
      #local Index=int((ValArr[I]-Min)/Width); // intervals and count them.
      #if (Index>=Intervals)
         #local Index=Index-1;
      #end
      #local HistArr[Index][1]=HistArr[Index][1]+1;
      #local I=I+1;
   #end
   #declare HistogramArray=HistArr
#end


// --------------------------------------------------------
// Trig:
// --------------------------------------------------------

#declare sind = function (V) {sin(radians(V))}
#declare cosd = function (V) {cos(radians(V))}
#declare tand = function (V) {tan(radians(V))}

#declare asind = function (V) {degrees(asin(V))}
#declare acosd = function (V) {degrees(acos(V))}
#declare atan2d = function (A, B) {degrees(atan2(A, B))}


// --------------------------------------------------------
// Misc:
// --------------------------------------------------------

#declare max3 = function (x, y, z) {max(x,y,z)}
#declare min3 = function (x, y, z) {min(x,y,z)}

#declare even = function(N) {select(mod(N, 2), 0, 1, 0)}
#declare odd  = function(N) {select(mod(N, 2), 1, 0, 1)}

// Squares the value
#declare f_sqr = function (V) {(V*V)}

// Returns the sign of a value
#declare sgn = function (V) {select(V,-1, 0, 1)}
//#declare sgn = function (V) {V/abs(V)}

// Range handling
// clips a number to the range [Min, Max]. Values above Max return Max,
// below Min return Min.
#declare clip = function (V, Mn, Mx) {min(Mx, max(V, Mn))}

// Clamps a number to the range [Min, Max].
// Values outside this range wrap around.
#declare clamp = function (V, Mn, Mx) {mod(V - Mn, Mx - Mn) + select(mod(V - Mn, Mx - Mn), Mx, Mn)}

// Adjusts input values in the range [0, 1] to output values in range [Rmn, Rmx].
#declare adj_range = function (V, Mn, Mx) {V*(Mx - Mn) + Mn}

// Adjusts values in a specified range [Rmn, Rmx] to the specified range [Min, Max]
#declare adj_range2 = function (V, Mn, Mx, OMn, OMx) {((V - Mn)/(Mx - Mn))*(OMx - OMn) + OMn}

// Interpolate author: Margus Ramst
// Interpolation
// GC - global current
// GS - global start
// GE - global end
// TS - target start
// TE - target end
// Method - interpolation method:
//          Method = 0 - cosine interpolation
//          Method > 0 - exponential (1 - linear, etc)
#macro Interpolate(GC, GS, GE, TS, TE, Method)
   (#if(Method!=0)
      (TS+(TE-TS)*pow((GC-GS)/(GE-GS),Method))
   #else
      #local X=(GC-GS)/(GE-GS);
      #local F=(1-cos(X*pi))*.5;
      (TS*(1-F)+TE*F)
   #end)
#end

// --------------------------------------------------------
// Vector macros:
// --------------------------------------------------------

// Squares the components of a vector
#macro VSqr(V) (V*V) #end

// Raises the components of a vector to a given power
#macro VPow(V, P) <pow(V.x, P), pow(V.y, P), pow(V.z, P)> #end
#macro VPow5D(V, P) <pow(V.x, P), pow(V.y, P), pow(V.z, P), pow(V.filter, P), pow(V.transmit, P)> #end

// Returns true if vectors are equal, otherwise false
#macro VEq(V1, V2) (V1.x = V2.x & V1.y = V2.y & V1.z = V2.z) #end
#macro VEq5D(V1, V2)
   ( V1.x = V2.x
   & V1.y = V2.y
   & V1.z = V2.z
   & V1.filter = V2.filter
   & V1.transmit = V2.transmit)
#end

// Returns true if vector is <0,0,0>, otherwise false
#macro VZero(V1) (V1.x = 0 & V1.y = 0 & V1.z = 0) #end
// Returns true if vector is <0,0,0,0,0>, otherwise false
#macro VZero5D(V1) (V1.x = 0 & V1.y = 0 & V1.z = 0 & V1.filter = 0 & V1.transmit = 0) #end

#macro VLength5D(V) sqrt(V.x*V.x + V.y*V.y + V.z*V.z + V.filter*V.filter + V.transmit*V.transmit) #end

#macro VNormalize5D(V) (V/sqrt(V.x*V.x + V.y*V.y + V.z*V.z + V.filter*V.filter + V.transmit*V.transmit)) #end

#macro VDot5D(V1, V2) (V1.x*V2.x + V1.y*V2.y + V1.z*V2.z + V1.filter*V2.filter + V1.transmit*V2.transmit) #end

// Cosine of angle between V1 and V2
#macro VCos_Angle(V1, V2) vdot(vnormalize(V1), vnormalize(V2)) #end

// Angle in radians between V1 and V2
#macro VAngle(V1, V2) acos(min(1, vdot(vnormalize(V1), vnormalize(V2)))) #end
// Angle in degrees between V1 and V2
#macro VAngleD(V1, V2) degrees(acos(min(1,vdot(vnormalize(V1), vnormalize(V2))))) #end

// VRotation() will find the rotation angle from V1 to V2
// around Axis. Axis should be perpendicular to both V1
// and V2. The output will be in the range between -pi and
// pi radians or between -180 degrees and 180 degrees if
// you are using the degree version. However, if Axis is
// set to <0,0,0> the output will always be positive or
// zero, the same result you will get with the VAngle() macros.
// Author: Rune S. Johansen
#macro VRotation(V1, V2, Axis)
   (acos(min(vdot(vnormalize(V1),vnormalize(V2)),1))
   *(vdot(Axis,vcross(V1,V2))<0?-1:1))
#end
#macro VRotationD(V1, V2, Axis)
   (degrees(acos(min(vdot(vnormalize(V1),vnormalize(V2)),1)))
   *(vdot(Axis,vcross(V1,V2))<0?-1:1))
#end

// Distance between V1 and V2
#macro VDist(V1, V2) vlength(V1 - V2) #end

// Returns a vector perpendicular to V
// Author: Tor Olav Kristensen
#macro VPerp_To_Vector(v0)
   #if (vlength(v0) = 0)
      #local vN = <0, 0, 0>;
   #else
      #local Dm = min(abs(v0.x), abs(v0.y), abs(v0.z));
      #if (abs(v0.z) = Dm)
         #local vN = vnormalize(vcross(v0, z));
      #else
         #if (abs(v0.y) = Dm)
            #local vN = vnormalize(vcross(v0, y));
         #else
            #local vN = vnormalize(vcross(v0, x));
         #end
      #end
   #end
   vN
#end

// Returns a vector perpendicular to V1 and V2
#macro VPerp_To_Plane(V1, V2) (vnormalize(vcross(V1, V2))) #end

// Find a vector perpendicular to Axis and in the plane of
// V1 and Axis. In other words, the new vector is a version
// of V1 adjusted to be perpendicular to Axis.
#macro VPerp_Adjust(V, Axis)
   vnormalize(vcross(vcross(Axis, V), Axis))
#end

// Projects a vector onto the plane defined by Axis.
// Based on code by Ron Parker
#macro VProject_Plane(V, Axis)
   #local A = vnormalize(Axis);
   (V - vdot(V, A)*A)
#end

// Projects a vector onto the an axis.
// Based on code by Ron Parker
#macro VProject_Axis(V, Axis)
   (Axis*vdot(V, Axis)/vdot(Axis, Axis))
#end

// Smallest component of V
#macro VMin(V) (min3(V.x, V.y, V.z)) #end

// Largest component of V
#macro VMax(V) (max3(V.x, V.y, V.z)) #end

// Creates a vector going in the direction of the
// given vector with the specified length
#macro VWith_Len(V, Len) (Len*vnormalize(V)) #end

// --------------------------------------------------------
// Vector analysis macros
// --------------------------------------------------------
// Authors: Christoph Hormann and Tor Olav Kristensen

// Various functions of vector analysis in form of macros
// that can be used in user defined functions or expressions
//
// all macros make use of a constant named
// '__Gradient_Fn_Accuracy_' for numerical approximation
// of the derivatives.
// This constant can be changed with the
// 'SetGradientAccuracy()' macro, the default value is 0.001.
//
// Because vector functions can only be created as pigment
// or transform/spline functions and can not be passed as
// a macro parameter there is no fn_Curl() function and the
// divergence and curl macros use 3 float functions for
// defining the vector field.

#ifndef (__Gradient_Fn_Accuracy_)
   #declare __Gradient_Fn_Accuracy_=0.001;
#end

#macro SetGradientAccuracy(Value)
   #declare __Gradient_Fn_Accuracy_=abs(Value);
#end

// macro calculating the gradient of a function
// as a function
//
// Parameters:
//     __Gradient_Fn: function to calculate the gradient from
//
// Output: the length of the gradient as a function
#macro fn_Gradient(__Gradient_Fn)

   function {
      f_r(
         __Gradient_Fn(x + __Gradient_Fn_Accuracy_, y, z) - __Gradient_Fn(x - __Gradient_Fn_Accuracy_, y, z),
         __Gradient_Fn(x, y + __Gradient_Fn_Accuracy_, z) - __Gradient_Fn(x, y - __Gradient_Fn_Accuracy_, z),
         __Gradient_Fn(x, y, z + __Gradient_Fn_Accuracy_) - __Gradient_Fn(x, y, z - __Gradient_Fn_Accuracy_)
      )/(2*__Gradient_Fn_Accuracy_)
   }

#end

// macro calculating the gradient of a function
// in one direction as a function
//
// Parameters:
//     __Gradient_Fn:  function to calculate the gradient from
//     Dir:            direction to calculate the gradient
//
// Output: the gradient in that direction as a function
#macro fn_Gradient_Directional(__Gradient_Fn, Dir)

   #local Dirx = vnormalize(Dir).x;
   #local Diry = vnormalize(Dir).y;
   #local Dirz = vnormalize(Dir).z;

   function {
      (
         (__Gradient_Fn(x + __Gradient_Fn_Accuracy_, y, z) - __Gradient_Fn(x - __Gradient_Fn_Accuracy_, y, z))*Dirx +
         (__Gradient_Fn(x, y + __Gradient_Fn_Accuracy_, z) - __Gradient_Fn(x, y - __Gradient_Fn_Accuracy_, z))*Diry +
         (__Gradient_Fn(x, y, z + __Gradient_Fn_Accuracy_) - __Gradient_Fn(x, y, z - __Gradient_Fn_Accuracy_))*Dirz
      )/(2*__Gradient_Fn_Accuracy_)
   }

#end

// macro calculating the divergence of a (vector) function
// as a function
//
// Parameters:
//     __Gradient_Fnx,
//     __Gradient_Fny,
//     __Gradient_Fnz: x, y and z components of a vector function
//
// Output: the divergence as a function
#macro fn_Divergence(__Gradient_Fnx, __Gradient_Fny, __Gradient_Fnz)

   function {
      (
       __Gradient_Fnx(x + __Gradient_Fn_Accuracy_, y, z) - __Gradient_Fnx(x - __Gradient_Fn_Accuracy_, y, z)+
       __Gradient_Fny(x, y + __Gradient_Fn_Accuracy_, z) - __Gradient_Fny(x, y - __Gradient_Fn_Accuracy_, z)+
       __Gradient_Fnz(x, y, z + __Gradient_Fn_Accuracy_) - __Gradient_Fnz(x, y, z - __Gradient_Fn_Accuracy_)
      )/(2*__Gradient_Fn_Accuracy_)
   }

#end

// macro calculating the gradient of a function
// as a vector expression
//
// Parameters:
//     __Gradient_Fn: function to calculate the gradient from
//     p0:            point where to calculate the gradient
//
// Output: the gradient as a vector expression
#macro vGradient(__Gradient_Fn, p0)

   (
    <
     __Gradient_Fn(p0.x + __Gradient_Fn_Accuracy_, p0.y, p0.z) - __Gradient_Fn(p0.x - __Gradient_Fn_Accuracy_, p0.y, p0.z),
     __Gradient_Fn(p0.x, p0.y + __Gradient_Fn_Accuracy_, p0.z) - __Gradient_Fn(p0.x, p0.y - __Gradient_Fn_Accuracy_, p0.z),
     __Gradient_Fn(p0.x, p0.y, p0.z + __Gradient_Fn_Accuracy_) - __Gradient_Fn(p0.x, p0.y, p0.z - __Gradient_Fn_Accuracy_)
    >/(2*__Gradient_Fn_Accuracy_)
   )

#end

// macro calculating the curl of a (vector) function
// as a vector expression
//
// Parameters:
//     __Gradient_Fnx,
//     __Gradient_Fny,
//     __Gradient_Fnz: x, y and z components of a vector function
//     p0:             point where to calculate the curl
//
// Output: the curl as a vector expression
#macro vCurl(__Gradient_Fnx, __Gradient_Fny, __Gradient_Fnz, p0)

  (
    <
      __Gradient_Fnz(p0.x, p0.y + __Gradient_Fn_Accuracy_, p0.z) - __Gradient_Fnz(p0.x, p0.y - __Gradient_Fn_Accuracy_, p0.z) -
      __Gradient_Fny(p0.x, p0.y, p0.z + __Gradient_Fn_Accuracy_) + __Gradient_Fny(p0.x, p0.y, p0.z - __Gradient_Fn_Accuracy_),

      __Gradient_Fnx(p0.x, p0.y, p0.z + __Gradient_Fn_Accuracy_) - __Gradient_Fnx(p0.x, p0.y, p0.z - __Gradient_Fn_Accuracy_) -
      __Gradient_Fnz(p0.x + __Gradient_Fn_Accuracy_, p0.y, p0.z) + __Gradient_Fnz(p0.x - __Gradient_Fn_Accuracy_, p0.y, p0.z),

      __Gradient_Fny(p0.x + __Gradient_Fn_Accuracy_, p0.y, p0.z) - __Gradient_Fny(p0.x - __Gradient_Fn_Accuracy_, p0.y, p0.z) -
      __Gradient_Fnx(p0.x, p0.y + __Gradient_Fn_Accuracy_, p0.z) + __Gradient_Fnx(p0.x, p0.y - __Gradient_Fn_Accuracy_, p0.z)
    >/(2*__Gradient_Fn_Accuracy_)
  )

#end

// macro calculating the divergence of a (vector) function
// as a float expression
//
// Parameters:
//     __Gradient_Fnx,
//     __Gradient_Fny,
//     __Gradient_Fnz: x, y and z components of a vector function
//     p0:             point where to calculate the divergence
//
// Output: the divergence as a float expression
#macro Divergence(__Gradient_Fnx, __Gradient_Fny, __Gradient_Fnz, p0)

   (
    (
     __Gradient_Fnx(p0.x + __Gradient_Fn_Accuracy_, p0.y, p0.z) - __Gradient_Fnx(p0.x - __Gradient_Fn_Accuracy_, p0.y, p0.z)+
     __Gradient_Fny(p0.x, p0.y + __Gradient_Fn_Accuracy_, p0.z) - __Gradient_Fny(p0.x, p0.y - __Gradient_Fn_Accuracy_, p0.z)+
     __Gradient_Fnz(p0.x, p0.y, p0.z + __Gradient_Fn_Accuracy_) - __Gradient_Fnz(p0.x, p0.y, p0.z - __Gradient_Fn_Accuracy_)
    )/(2*__Gradient_Fn_Accuracy_)
   )

#end

// macro calculating the length of the gradient
// of a function as a float expression
//
// Parameters:
//     __Gradient_Fn:  function to calculate the gradient from
//     p0:             point where to calculate the gradient
//
// Output: the length of the gradient as a float expression
#macro Gradient_Length(__Gradient_Fn, p0)
   vlength(vGradient( function { __Gradient_Fn(x, y, z) } , p0))
#end

// macro calculating the gradient of a function
// in one direction as a float expression
//
// Parameters:
//     __Gradient_Fn:  function to calculate the gradient from
//     p0:             point where to calculate the gradient
//     Dir:            direction to calculate the gradient
//
// Output: the gradient in that direction as a float expression
#macro Gradient_Directional(__Gradient_Fn, p0, Dir)
   vdot(
      vGradient( function { __Gradient_Fn(x, y, z) }, p0),
      vnormalize(Dir)
   )
#end

#version MATH_INC_TEMP;
#end//math.inc

