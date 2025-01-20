# Software Architecture:
<img src="./UML_answer.png">

## Refactoring:
The current service criteria are as follows:
- Engines
  - Capulet Engine - should be serviced once every 30,000 miles
  - Willoughby Engine - should be serviced once every 60,000 miles
  - Sternman Engine - should be serviced only when the warning indicator is on

- Batteries
  - Spindler Battery - should be serviced once every 2 years
  - Nubbin Battery - should be serviced once every 4 years


## The current car models are as follows:
 - Calliope
    - Capulet Engine
    - Spindler Battery
 - Glissade
    - Willoughby Engine
    - Spindler Battery
 - Palindrome
    - Sternman Engine
    - Spindler Battery
 - Rorschach
    - Willoughby Engine
    - Nubbin Battery
 - Thovex
    - Capulet Engine
    - Nubbin Battery

## Unit test:
 - Replaced the old test suite in the tests folder with new series of unit tests.

# Test-driven development:
- a. upgrade spindler batteries
Modified the Spindler battery so it requires service after three years instead of two. Notice how easy it is to make this change - ONLY need to touch one line of code instead of several, and the place where that line of code lives is immediately obvious..

- b. add tire servicing criteria
There are two types of tires currently in use by the Lyft fleet - Carrigan tires and Octoprime tires. The new tire wear sensors produce an array of four numbers between 0 and 1 inclusive, representing how worn each of the tires are. This array will be passed to each function in the car factory class, to be used by your tire implementation. Carrigan tires should be serviced only when one or more of the values in the tire wear array is greater than or equal to 0.9. Octoprime tires should be serviced only when the sum of all values in the tire wear array is greater than or equal to 3. 
