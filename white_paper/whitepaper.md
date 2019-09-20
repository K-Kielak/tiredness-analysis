# Teyered – An Effective Solution to Drowsiness Detection

{{TOC}}

### Guide: asdasd

```
*Bold*: Looking for a better word.
#TODO: Must be fixed\
`Comments`
```

### Outline:

1. **Summary / Synopsis**

2. **Introduction to the problem**
   
   1. **General Research about Problem**

Safety is the most essential priority while driving. Drowsiness on the wheel however,  endangers both drivers and pedestrians and is  among the leading causes for car accidents. About 17% of fatal traffic accidents are estimated to be due to tiredness (AAA, 2010) which results in an estimated yearly cost of $43.15 - $56.02 billion in the United States alone (Leger, 1994). 

#todo Change figures or improve wordings

Additionally, drowsiness has been demonstrated to severely impair driving performance. On average, tired drivers perform worse than alcohol-intoxicated individuals with blood alcohol concentration of 0.05% (Williamson et al., 2000). 
   
   2. **Relating Back to industry (Loss to Stakeholders)**

Predicting dangerous levels of tiredness and preventing vehicle crashes or accidents offer a business opportunity to produce safer vehicles, decrease insurance costs as well as possibly saving lives. 

The automotive industry has reacted to the drowsiness problem by introducing drowsiness-detection systems. These systems consider  four main categories of patterns:
#TODO subjective, vehicle, face/eyes and other physiological patterns. 

   3. **Problem Statement** 

This paper will consider existing approaches and patterns for drowsiness detection as well as their effectiveness, and provides a `Try to soft sell your solution`


3. **Detection (Review)**
   
   
   1. **The biology of tiredness**

Drowsiness is the tendency of an individual to fall asleep. There are three main phases of sleep: awake, Non-Rapid Eye Movement (NREM) sleep and Rapid Eye Movement (REM) sleep. 

NREM can then be subdivided three stages by using brain waves data from electroenephalograms (EEG) (Brodbeck et al., 2012):

	- Stage 1: Awake to Asleep transition (drowsy)
	- Stage 2: Light Sleep
	- Stage 3: Deep Sleep
	

Drowsiness detection methods typically attempt at detecting the early stages of NREM. 

Drowsiness-related accidents show recurring characteristics. They occur primarily late at night (0:00 AM – 7:00 AM) or in the early afternoon (2:00 PM – 4:00 PM). Usually there are no signs of vehicle defects or breaks usage and the weather conditions are generally good with clear visibility (Sahayadhas et al., 2012). 

Additionally, studies by Philip et al. (2005) and Thiffault et al. (2001) have identified the monotony of the road environment  as a possible trigger for drowsiness. Moreover, signs of drowsiness based on the drivers performance can be observed within 20-25 minutes of driving (Philip et al., 2005).

   2. **Drowsiness Measurement Techniques**  
      
      - **General Approach (and why they are bad)**

Drowsiness detection systems generally consist of a device that is embedded in the vehicle and monitors the driver. The device captures data in the form of pictures from a camera or sensors such as steering wheel sensors. The data is then processed and analysed by an algorithm to measure the drowsiness level. This process can be repeated a multiple times for a certain length of time `t` (Figure 1). 

/img/detection.png
```
digraph Figure1 {

"Data Capturing" -> "Data Pre-Processing" -> "Drowsiness analysis";
"Data Capturing" -> "Data Capturing" [style=dashed, label="  t"]

}
```
**Figure 1.** A general diagrammatic representation of the drowsiness analysis process. When data is recorded, it is then preprocessed and used for drowsiness analysis. The process is usually repeated over time (dashed line labeled `t`). 

This process is adapted in different ways depending on the type of data being collected, which is either: subjective, vehicle-based, image-based or physiological. 

  - **Existing Approaches (and why they are bad)**

## 2.1 Subjective Measures 

Subjective measures involve the driver’s own assessment of their alertness level. The Karolinska Sleepiness Scale (KSS) is a nine-point scale and it is the most widely used scales to describe drowsiness (Shahid et al., 2011). Each rating of the KSS has an associated description as shown in Table 1.

| Rating | Description |
|:--|:--|
| 1 | Extremely alert |
| 2 | Very alert |
| 3 | Fairly alert |
| 4 | Alert |
| 5 | Neither alert nor sleepy |
| 6 | Some signs of sleepiness |
| 7 | Sleepy but no effort to keep alert |
| 8 | Sleepy some effort to keep alert |
| 9 | Very Sleepy, great effort to keep alert, fighting sleep |

**Table 1.** The Karolinska Sleepiness Scale (KSS) with descriptions for each rating. 

The KSS has been used to monitor the driver’s drowsiness level in driving simulations and compared to other sources of data such as EEG data (Hu et al., 2009) or Lane Position data (Sommer et al., 2010). The results however, were mixed and they largely depend on the driver’s consistence in the self-assessment. This method may not be consistent between different drivers and may also fail to capture sudden changes in drowsiness levels due to micro-sleep events (Sahayadhas et al., 2012). 

An additional limitation it is difficult to inquire the driver while driving on a real road, and in addition to being a source of distraction, it may indirectly alert the driver, affecting their drowsiness level (Sahayadhas et al., 2012). 


## 2.2 Vehicle-Based Measures

Vehicle-based measures aim at determining drowsiness level via the interaction between the driver and the vehicle. These usually involve sensors such as steering wheel sensors or lane position sensors. 

### Steering Wheel Sensors

These sensors measure the change in angle of the steering wheel. There are two main phases of drowsiness that can be detected with steering wheel sensors: 

 - **Phase 1**: Early-stage drowsiness where the driver is unable to smoothly control the vehicle, with large manoeuvres to correct the vehicle position. This usually results in zigzag driving and has been reported by multiple research studies (Sayed et al., 2001; Eskandarian et al., 2007)
 - **Phase 2**: The dozing off phase. The driver stops reacting to feedback from the road, therefore the steering sensors have a flat and constant value which is usually combined with an increase lateral position (Eskandarian et al., 2007).

Typically, these two phases alternate each other in drowsy individual, right before a crash (Figure #todo )

/img/steering.png

**Figure** #Todo. Steering wheel angle patterns in a 5 km drive simulation. There are two main phases: Phase 1 characterised by large changes in steering angles and Phase 2 with rather constant values. *Figure adapted from Eskandarian et al., 2007*.

Other measures that can be calculated from steering sensors are the Standard Deviation of Angular Velocity (SDAV) of the steering wheel and the proportion of STeering wheel movements EXceeding Three degrees (STEX3). These are highly correlated to Psychomotor Vigilance Tests and the KSS scale (Forsman et al., 2013). 

These sensors work well with steering angles between 0.5° - 5.0°  . Steering Wheel Metrics are too dependent on roads with specific geometries and may be affected by the vehicle kinetics in particular environments (Eskandarian et al., 2007). Additionally, monotonous roads such as straight roads, provide little to no variation to be detected  which may result in drowsiness not being detected. Monotonous roads are also among the roads with the highest number of accidents so this solution might not be as accurate as others (Eskandarian et al., 2007).


- Lateral lane position
- Steering wheel variability 
- Steering wheel three degree angle  

## 2.3 Image-Based Measures

- Eyes
	- Perclos
	- Average Eye Closure Speed
	- Delay of eyelid reopening
- Blinks
	- Blink Frequency
	- Blink Duration
- Gaze
	- Eye Gaze
- Mouth
	- Mouth Openness

Image based techniques involve a device that records the drivers face. A set of features are extracted from the pictures which can be correlated to tiredness, such as for example, eyes closed for a prolonged period of time. 

## 2.4 Physiological Measures: 
- EEG
- ECG
- Heart Rate
   
   3. Recommended (*our*) Solution 
      
      - Must be in generic terms as it aims at educating rather than selling
   4. Case Study / Statistics (optional)

4. **Conclusion**
   
   1. Ideal Solution Characteristics (bullet points / table)
      
      - Most important part of white paper. 
      
      - Must set distance from competition without sounding like a pitch
      
      - The name of our solution must be mentioned after the bullet points
   
   2. Call to Action
      
      - Where to find more information
      
      - Next steps of buying process
   
   3. About 
      
      - Brief Description of company + website 
      
      - Names (+ descriptions optionally) of the researchers.







---- Text that can be useful but likely unusable ---- 

Tiredness on the wheel is the cause of TODO number of accidents every year and endangers the lives of both drivers and pedestrians (TODO: Add citation). 

Since the past years, the automotive industry has attempted to tackle this issue with drowsiness-detection systems that have been embedded in vehicles. These systems are however outdated, and recent advances in machine learning have allowed the detection of more complex and personalized patterns of tiredness. 

Osmitau Technologies **delivers** Teyered, an adaptable drowsiness-detection systems that uses state-of-the-art techniques to prevent road accidents. 

This offers an opportunity to provide customers with safer vehicles 

Teyered combines different sources of inputs, learns new patterns and adapts to the driver.



Sources: 

AAA 2010 - https://aaafoundation.org/prevalence-impact-drowsy-driving/
Leger 1994 - https://academic.oup.com/sleep/article/17/1/84/2749451
Williamson 2000 - https://oem.bmj.com/content/57/10
Brodbeck 2012 - https://www.sciencedirect.com/science/article/abs/pii/S1053811912005484?via%3Dihub
Sahayadhas 2012 - https://www.mdpi.com/1424-8220/12/12/16937/htm
Philip 2005 - https://www.ncbi.nlm.nih.gov/pubmed/15784201
Thiffault 2003 - https://www.ncbi.nlm.nih.gov/pubmed/12643955
Shahid 2011- https://link.springer.com/chapter/10.1007/978-1-4419-9893-4_47
Hu 2009 https://dl.acm.org/citation.cfm?id=1508574
Sayed 2001 - https://journals.sagepub.com/doi/10.1243/0954407011528536

Forsman 2013 - https://www.sciencedirect.com/science/article/pii/S0001457512001571