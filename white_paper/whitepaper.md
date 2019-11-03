# Teyered – An Effective Solution to Drowsiness Detection

{{TOC}}

### Guide:

```
*Bold*: Looking for a better word.
#TODO: Must be fixed
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

This process is adapted in different ways depending on the type of data being collected, which is either: subjective, vehicle-based, behavioural or physiological. 

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

These sensors work optimally with steering angles between 0.5° - 5.0°  and they are also relatively easy to install on vehicles. Steering wheel metrics however, are too dependent on roads with specific geometries and may be affected by the vehicle kinetics in particular environments (Eskandarian et al., 2007).          Additionally, monotonous roads such as straight roads, provide little to no variation to be detected  which may result in drowsiness not being detected. Steering wheel sensors may also fail to detect changes in relatively straight roads or highly trafficked roads, which are among the roads with the highest number of accidents (Eskandarian et al., 2007).

### Lane Position Sensors 

 Lane position sensors involve a combination of an external camera and lane-tracking algorithms. Then, the position of the vehicle can be calculated with respect to the lanes (Ingre et al., 2006). 
 
 Patterns that can be calculated from this type of data are: Standard Deviation of Lane Position (SDLP), Lateral Lane Position and the Frequency of Abnormal Lane Deviation (Ingre et al., 2006; Cheng et al., 2012; Sun et al., 2017).  In their research, Ingre et al. (2006) found significant correlation between the KSS scale and both the SDLP (Figure #todo) and the blink duration (discussed in the next section).
 
/img/lane_position.png

**Figure** #todo . Positive correlation between the Standard Deviation of Lane Position (SDLP) and the Karolinska Sleepiness Scale (KSS) (n = 20). The estimated fixed effect (thick) shows a peak in drowsiness (KSS 8-9) between SDLP of 0.36 and 0.40.

 Limitations of this method include the dependency on road marks for lane detection, lighting and weather conditions (Sahayadhas et al., 2012). Additionally, the decrease in driving performance may not be uniquely due to drowsiness. An alternative root cause for example, may be the driver’s years of experience which may directly impact the driving performance.
 
## 2.3 Behavioural Measures

Behavioural measures attempt at identifying behaviours associated with drowsiness. Behavioural measures usually rely on a camera that records the drivers face. A set of features are extracted from the pictures which can be correlated to drowsiness, such as for example, closed eyes for a prolonged period of time. 

The majority of the features correlated with drowsiness are obtained from the head, the mouth or the eyes.

### Head Features 

Drowsy drivers seem to sway their heads (Sahayadhas et al., 2012), increase nodding, scratch their face more frequently and more prone to rotate their heads to the left to relieve tension on the neck (Eskandarian et al., 2007). The head position can also be used to calculate the slouching and posture adjustment frequency. The features involving rotations are quantifiable with available face detection methods (#todo CITE). Other behaviours like scratching may be harder to quantify and may not be consistent across different individuals. 

### Mouth Features 

Yawns are the most common mouth features correlated with drowsiness. This is usually measured as the degree of mouth openness which will vary if the driver is normal, drowsy or just talking (Wang et al., 2006). 

### Eyes Features 

Eyes, and more specifically blinking, have been studied extensively for drowsiness detection. The most commonly used approach is PERCLOS, the PERcentage of eyes CLOSure over a time period and has been shown to be very effective in drowsiness detection (Sahayadhas et al., 2012). A more recent study by Trutschel et al. (2017) however, challenged the effectiveness of PERCLOS and commercially available PERCLOS-based systems. In a trial with three commercial systems, PERCLOS had a higher error rate in drowsiness detection of about 10% compared to EEG data (Trutschel et al., 2017). This has been associated episodes of microsleep events where drivers are asleep with their eyes open which PERCLOS fails to address (Trutschel et al., 2017)

Alternative eye features correlated with drowsiness include the Average Eye Closure Speed (AECS), Blink Frequency and Duration and pupil diameter (Wang et al., 2006). Additionally, eye gaze can also be extracted to verify whether the driver is looking at the road ahead (Wang et al., 2006).

#todo picture of blinks or some other picture

Once these features are extracted, a threshold is set to classify the driver as drowsy or not. Given that most of these features rely on a temporal dimension, they tend to perform better when used for a longer period of time (Wilkinson et al., 2013). 

The main limitation of behavioural approaches is the camera as it is significantly affected by the light conditions. This has partially been minimised by the addition of an infrared camera(Sahayadhas et al., 2012). However, the systems may still be sensitive to sudden changes in illumination or dust accumulating on the camera sensor which may affect the feature detection steps.

## 2.4 Biological Measures: 

Biological measures focus on the detecting significant changes in physiological signals as measured by electrocardiogram (ECG),   electroencephalogram (EEG), electro-oculography (EOG), surface electromyogram (sEMG) (Dong et al., 2011). 

EEG has been studied extensively, as it detects brain waves related to sleep (Qiong et al., 2006). Drowsiness is usually correlated with an increase of a continuous signal of α and θ waves compared to β waves, detectable with the formula (α + θ)/β (Dong et al., 2011). Although very accurate, EEG measurements are very invasive, consisting in electrodes in contact with the skin (Dong et al., 2011). Nonetheless it has been very useful to evaluate other measures of drowsiness such as Standard Deviation of Steering Wheel Angle and Lateral Lane Position (Boyle et al., 2008). 
   
   
   
   
   
   3. Recommended Hybrid (*our*) Solution 
      
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
ingre 2006 https://www.ncbi.nlm.nih.gov/pubmed/16490002
cheng et al 2012 https://onlinelibrary.wiley.com/doi/abs/10.1002/hfm.20395
wang et al 2006 - https://ieeexplore.ieee.org/abstract/document/1713656

wilinkson 2013 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3836343/
Trutschel 2017  10.17077/drivingassessment.1394

Dong, Y., Hu, Z., Uchimura, K., & Murayama, N. (2011). Driver Inattention Monitoring System for Intelligent Vehicles: A Review. IEEE Transactions on Intelligent Transportation Systems, 12(2), 596–614. doi:10.1109/tits.2010.2092770

Qiong Wang, Jingyu Yang, Mingwu Ren, & Yujie Zheng. (2006). Driver Fatigue Detection: A Survey. 2006 6th World Congress on Intelligent Control and Automation. doi:10.1109/wcica.2006.1713656

boyle et al 2008 10.1016/j.trf.2007.08.001