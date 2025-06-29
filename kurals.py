import random
from datetime import date

kurals = [
    {
        "number": 1,
        "tamil": "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு",
        "english": "A is the first letter of all alphabets; it is the beginning of the world.",
        "explanation": "This verse speaks of the significance of the first letter in the alphabet, signifying the start of everything.",
        "modern_interpretation": "This can be seen as a reflection of how every beginning starts with a fundamental principle or foundation."
    },
    {
        "number": 2,
        "tamil": "பொதுவே உலகில் உள்ள எல்லா வாழ்க்கைகளும் உம்மை நம்பினால் வீழ்ச்சி வராது",
        "english": "All lives in the world will not perish if they believe in the truth.",
        "explanation": "This verse emphasizes the importance of faith in truth for the success and survival of life.",
        "modern_interpretation": "Having trust in the core values of truth and integrity ensures stability and success."
    },
    {
        "number": 3,
        "tamil": "அறத்தன்மையைப் பின்பற்றாதவரே திருட்டு செய்பவர்",
        "english": "Those who do not follow virtue are the ones who commit theft.",
        "explanation": "Thiruvalluvar compares the act of not living a virtuous life to stealing, as both are harmful to society.",
        "modern_interpretation": "Living without integrity or ethical values is akin to committing a personal theft of moral character."
    },
    {
        "number": 4,
        "tamil": "பிறர் வழியில் நடக்கும் யார் அந்த வழியில் தவிர்க்க வேண்டும்",
        "english": "Those who follow the path of others must avoid the path of harm.",
        "explanation": "This verse talks about the importance of being cautious when following others' advice and not falling into negative paths.",
        "modern_interpretation": "When following advice or trends, one must be discerning and avoid paths that lead to negativity or harm."
    },
    {
        "number": 5,
        "tamil": "நன்றி என்பது நல்ல செயலைச் செய்தவனைப் போற்றுவதும் ஆகும்",
        "english": "Gratitude is the act of honoring the one who has done good to us.",
        "explanation": "Gratitude is a key virtue, and this verse emphasizes honoring those who help and do good deeds for others.",
        "modern_interpretation": "Being thankful and showing appreciation towards those who help you is essential for a positive and healthy relationship."
    },
    {
        "number": 6,
        "tamil": "உலகில் தோல்வியுற்றவன் சுயக்கடமைக்கு வழியைக் காட்டினால் அது வாழ்க்கையின் சீரான வழி ஆகும்",
        "english": "A person who shows others the way to self-discipline will be respected and honored in this world.",
        "explanation": "This verse highlights the importance of guiding others toward self-discipline and virtue, which ultimately leads to respect.",
        "modern_interpretation": "Leading by example in matters of discipline and self-improvement brings admiration and success."
    },
    {
        "number": 7,
        "tamil": "பிறன் பயன் அரிது எனும் பழிவாங்கி உன்னுடைய ஆக்கத்தை பாதுகாப்பது",
        "english": "It is rare to find someone who appreciates your efforts without personal motives.",
        "explanation": "This verse speaks to the rarity of true selflessness and how many people act with their own interests in mind.",
        "modern_interpretation": "True, unbiased appreciation for someone else's efforts is hard to come by in today's world."
    },
    {
        "number": 8,
        "tamil": "வாழ்க்கையில் ஒருவரின் உயிரினி வாழ்வதற்காகவோ வாழும் என்று கூறினால் அது செயல் அல்ல",
        "english": "A life lived for mere existence is not a true life, for it lacks purpose and action.",
        "explanation": "This verse stresses the importance of living life with purpose and not just for survival.",
        "modern_interpretation": "Living with intention, passion, and purpose is what gives life meaning beyond just existing."
    },
    {
        "number": 9,
        "tamil": "அன்புள்ளவரின் செயல் அவனுக்கே ஒரு பலன் தரும்",
        "english": "A person’s actions done with love will always result in rewards for the person.",
        "explanation": "This verse highlights the reciprocal nature of love and virtuous deeds, where good actions will eventually return good to the doer.",
        "modern_interpretation": "When you act with love and sincerity, the results will naturally benefit you, whether immediately or over time."
    },
    {
        "number": 10,
        "tamil": "நெஞ்சத்தில் ஒழுக்கங்களை உணர்ந்தவர் உலகின் மேலானவர்",
        "english": "Those who feel the power of virtue in their hearts are the greatest among all.",
        "explanation": "This verse emphasizes that true greatness comes from the internal realization and practice of virtue, not external accolades.",
        "modern_interpretation": "True greatness is internal, stemming from personal integrity, wisdom, and self-awareness."
    },
    {
        "number": 11,
        "tamil": "அவர் கண்ணில் பிணி இல்லாத பத்து அறன்கள் விருதுகள் ஆகும்",
        "english": "The ten virtues that have no flaws are the most rewarding in life.",
        "explanation": "This verse lists the ten virtues that are essential for living a righteous and meaningful life.",
        "modern_interpretation": "Living a virtuous life free of flaws brings great rewards in both the material and spiritual realms."
    },
    {
        "number": 12,
        "tamil": "சில நேரங்களில் தன் பகையை விட அதற்குரிய விரும்பத்தைக் கொள்கிறார்",
        "english": "Sometimes one becomes more eager for something than one’s own enemies.",
        "explanation": "This verse speaks about the strong desires people sometimes have that surpass even the antagonism of their enemies.",
        "modern_interpretation": "Desires and ambitions can sometimes overshadow any external opposition, even that of enemies."
    },
    {
        "number": 13,
        "tamil": "எது சொல்வதென்று பிறர் மாறாக்கிறார்",
        "english": "When others become disturbed by your words, you must choose your words wisely.",
        "explanation": "This verse advises caution in speech, as words can influence others' emotions and thoughts.",
        "modern_interpretation": "One should be mindful of what they say, as words have a strong impact on others."
    },
    {
        "number": 14,
        "tamil": "கேட்டும் புலன்கள் பொருளடக்கம் காட்டுவிடும்",
        "english": "One must listen to what the senses are saying about the truth of a matter.",
        "explanation": "This verse stresses the importance of being aware of the senses and using them to discern truth.",
        "modern_interpretation": "Awareness and perception through the senses lead to better understanding and decisions."
    },
    {
        "number": 15,
        "tamil": "எல்லாவற்றுக்கும் அவன் பண்பு போற்றப்படவேண்டும்",
        "english": "Everything must be done according to one’s character, as character is the ultimate guide.",
        "explanation": "This verse speaks to the importance of having a good character, as it guides all actions and decisions.",
        "modern_interpretation": "Character is the foundation of every decision and action—let your actions reflect your values."
    },
    {
        "number": 16,
        "tamil": "பட்டம் பேசும் போது எதிரிகள் வெறுக்கின்றனர்",
        "english": "When one speaks of wisdom, enemies often despise it.",
        "explanation": "This verse acknowledges that those who speak of wisdom may face resentment from those who are not wise.",
        "modern_interpretation": "Wisdom is often met with resistance, but those who are wise must not be deterred by criticism."
    },
    {
        "number": 17,
        "tamil": "செயலுக்கே பயனாகும் அவன்",
        "english": "A person who does good for the sake of others, is sure to reap the benefits of those actions.",
        "explanation": "This verse emphasizes that selfless actions for the benefit of others will always lead to personal fulfillment.",
        "modern_interpretation": "Selfless service to others brings fulfillment and rewards that far exceed personal desires."
    },
    {
        "number": 18,
        "tamil": "மெய்யுள்ள நாதனும் உயர்ந்த வானுடையவனும் ஒருவன்",
        "english": "The person who possesses true wisdom and understanding is the highest among all.",
        "explanation": "This verse highlights that wisdom and understanding elevate a person beyond all others in true greatness.",
        "modern_interpretation": "True wisdom and understanding make a person truly great, transcending all superficial accolades."
    }
]

def get_kural_of_the_day():
    today = date.today()
    index = today.toordinal() % len(kurals)
    return kurals[index]
