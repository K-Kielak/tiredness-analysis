# Teyered – An Effective Solution to Drowsiness Detection

### Guide: asdasd

```
*Bold*: Looking for a better word.
#TODO: Must be fixed\
`Comments`
```

### Outline:

1. **Summary / Synopsis**

2. **Introduction to the problem**
   
   1. General Research about Problem

Safety is the most essential priority while driving. Drowsiness on the wheel however,  endangers both drivers and pedestrians and is  among the leading causes for car accidents. About 17% of fatal traffic accidents are estimated to be due to tiredness (AAA, 2010) which results in an estimated yearly cost of $43.15 - $56.02 billion in the United States alone (Leger, 1994). 

#todo Change figures or improve wordings

Additionally, drowsiness has been demonstrated to severely impair driving performance. On average, tired drivers perform worse than alcohol-intoxicated individuals with blood alcohol concentration of 0.05% (Williamson et al., 2000). 
   
   2. Relating Back to industry (Loss to Stakeholders)

Predicting dangerous levels of tiredness and preventing vehicle crashes or accidents offer a business opportunity to produce safer vehicles, decrease insurance costs as well as possibly saving lives. 

The automotive industry has reacted to the drowsiness problem by introducing drowsiness-detection systems. These systems consider  four main categories of patterns:
#TODO subjective, vehicle, face/eyes and other physiological patterns. 
   
   3. Problem Statement 

This paper will consider existing approaches and patterns for drowsiness detection as well as their effectiveness, and provides a `Try to soft sell your solution`


3. **Detection (Review)**
   
   
   1. The biology of tiredness

Drowsiness is the tendency of an individual to fall asleep. There are three main phases of sleep: awake, Non-Rapid Eye Movement (NREM) sleep and Rapid Eye Movement (REM) sleep. 

NREM can then be subdivided three stages by using brain waves data from electroenephalograms (EEG) (Brodbeck et al., 2012):

	- Stage 1: Awake to Asleep transition (drowsy)
	- Stage 2: Light Sleep
	- Stage 3: Deep Sleep
	

Drowsiness detection methods typically attempt at detecting the early stages of NREM. 

Drowsiness-related accidents show recurring characteristics. They occur primarily late at night (0:00 am–7:00 am) or in the early afternoon (2:00 pm–4:00 pm). Usually there are no signs of vehicle defects or breaks usage and the weather conditions are generally good with clear visibility (Sahayadhas et al., 2012). 

Additionally, studies by Philip et al. (2005) and Thiffault et al. (2001) have identified the monotony of the road environment  as a possible trigger for drowsiness. Moreover, signs of drowsiness based on the drivers performance can be observed within 20-25 minutes of driving (Philip et al., 2005).

   2. Drowsiness Detection Techniques  
      
      - Existing Approaches (and why they are bad)

The general consensus among drowsiness detection systems is that a device is embedded in the vehicle and monitors the driver by capturing data in the form of pictures or sensors such as steering wheel sensors. The data is then processed and analysed by an algorithm to determine the drowsiness level. This process can be repeated a multiple times for a certain amount of time `t` (Figure 1). 

/img/detection.png
```
digraph Figure1 {

"Data Capturing" -> "Data Pre-Processing" -> "Drowsiness analysis";
"Data Capturing" -> "Data Capturing" [style=dashed, label="  t"]

}
```
**Figure 1.** A general diagrammatic representation of the drowsiness analysis process. When data is recorded, it is then preprocessed and used for drowsiness analysis. The process is usually repeated over time (dashed line labeled `t`). 

This process is adapted in different ways depending on the type of data being collected, for example 
#TODO steering, vehicle-to-lane, face/eyes or other physiological measures. 

# 2.1 Subjective techniques 

- Questionnaire 

Talk about the guy that fell asleep in the car


# 2.2 Vehicle-Based Techniques

- Lateral lane position
- Steering wheel variability 
- Steering wheel three degree angle  

# 2.3 Image-Based Techniques

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

# 2.4 Physiologically-Based Techniques: 
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