import dspy
import re

class DaveBot():
    def get_feedback(self, essay, document):
        turbo = dspy.OpenAI(model='gpt-3.5-turbo-0125', max_tokens=1400)
        dspy.settings.configure(lm=turbo)
        essay = self.index_sentences(essay)
        class Marker(dspy.Signature):
            """Provide concise feedback to improve sentences in an IB History 12 essay. Reference each sentence by index and maintain numerical order. Be strict to encourage improvement, respond to 61% of sentences inside the essay. Feedback should be max 80 tokens for each sentence, include a score based on the rubric. Format: [index], feedback. Score: [range].
            """

            essay = dspy.InputField(desc="An essay with indexed sentences. Reference these when giving feedback.")
            rubric = dspy.InputField(desc="The rubric describing marking criteria and score ranges for each sentence.")
            feedback = dspy.OutputField(desc="List of feedback for individual sentences. Each feedback has such structure: {sentence_index}. {feedback_text}. Score: {score_range}")

        predict = dspy.Predict(Marker,  n=3)

        output = predict(essay=essay, rubric=document)
        
        largest = self.get_largest(output.completions.feedback)
    
        largest = self.parse_feedback_string(largest)
       
        final = self.create_feedback_dict(essay, largest)

        return final 

    def get_largest(self, listofString):
        if not listofString:
            return None  # Return None if the list is empty
        
        longest = listofString[0]  # Initialize with the first string
        for string in listofString[1:]:  # Start from the second string
            if len(string) > len(longest):
                longest = string  # Update longest if the current string is longer
        
        return longest

    def create_feedback_dict(self, annotated_essay, feedback_tuples):
        feedback_dict_sentences = {}
        sentence_pattern = re.compile(r'(.+?) \[(\d+)\]\.')

        for match in sentence_pattern.finditer(annotated_essay):
            sentence = match.group(1).strip()
            index = int(match.group(2))
            feedback = ""

            for tuple_index, tuple_feedback in feedback_tuples:
                if int(tuple_index) == index:
                    feedback = tuple_feedback.strip()
                    break

            sentence += '.'  # Add period at the end of the sentence
            feedback_dict_sentences[index] = (sentence, feedback)

        return feedback_dict_sentences

    def parse_feedback_string(self, feedback_string):
        feedback_list = feedback_string.split('\n')
        feedback_tuples = []

        for item in feedback_list:
            if item:
                index, feedback = item.split('. ', 1)
                feedback_tuples.append((index, feedback))

        return feedback_tuples
    
    def index_sentences(self, text):
        # Split the text into sentences using regular expressions
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        
        # Initialize an empty list to store indexed sentences
        indexed_sentences = []
        
        # Iterate through each sentence and append the index before the ending punctuation
        for i, sentence in enumerate(sentences, start=1):
            # Remove trailing whitespace
            sentence = sentence.strip()
            # Find the position of the ending punctuation
            end_punctuation_index = len(sentence) - 1
            while end_punctuation_index >= 0 and sentence[end_punctuation_index] not in '.?!':
                end_punctuation_index -= 1
            # Insert the sentence index before the ending punctuation
            indexed_sentence = f"{sentence[:end_punctuation_index]} [{i}]{sentence[end_punctuation_index:]}"
            indexed_sentences.append(indexed_sentence)
        
        # Join the indexed sentences back into a single string
        indexed_text = ' '.join(indexed_sentences)
        
        return indexed_text

# student_writing = """Discuss the failure and success of peacemaking in 2 wars. 


# Peacemaking after wars involves the creation of policies and conditions that guarantee that nations may coexist for a long period of time after the war. In terms of WW1 which ended in 1917, and WW2, which ended in 1945, peacemaking was not always successful as it encompassed a wide range of effects that involved the entire world. However, peacemaking was generally more successful after WW2 than WW1 in terms of economic effects, but both saw equal failures in terms of territorial effects. 


# To begin, peacemaking in terms of economics was much less successful after WW1 than in WW2. Peacemaking after WW1 saw the Treaty of Versailles (TOV, which was made by the winner of the war and was decidedly unfair to the losers: the Germans and the Austro-Hungarians). Articles 45 and 221 saw the war reparations that Germany had to pay after the war which amounted to 200 billion marks or over 800 billion dollars adjusted to inflation. Germany, not being abel to afford this, resulted to printing money and led to hyperinflation in Germany. Break worth 5 marks in 19919 skyrocketed to 200 billion marks per loaf; people lost jobs, pensions grew to nothing, and hte currently lost its value. As a result, people resorted to radical political options and elected the Nazi party in 1932. Many orthodox historians would argue that the Nazi party was to blame for WW2, therefore economic reforms after WW1 were mostly failures, Furthermore, other articles in the TOV articles in the TOV and other treaties led to reparations that were paid by Austria-Hungary, where a similar inflation ensured, eventually leading to the Anschluss between Germany before WW2. On the other hand, policies after WW2 were a major success. The partition of India in 1947 had some positive economic effects as 2 million educated Indians were displaced from West Punjab to East Punjba, This increase in the concentration of educated Indians led to great economic advancements such as GMO crops in the Green revolution that happened in the 1970s, propelling India to becoming a leader in terms of global wheat production. On the other hand, Germany also saw positive changes as the instalment of West Berlin saw great economic prosperity return to the area, Therefore, the economic effects of WW1 were generally less successful than the economic effects of WW2. 

# Contrastingly, the territorial changes after WW1 and WW2 were mostly failures. After WW1, article 245 of the TOV saw the war guilt clause where Germany was forced to pay with all her colonial possessions in addition to 15% of her mainland. These territorial changes allowed Hitler to use the notion of “lebensraum” to further support his expansionist viewpoints. Although historian Stephen Bungay argues that these concessions were generally good for slowing down the rearmament of Germany, the Appeasement that took p.ace in the late 1930s rendered this war guild useless as nearly all of Germany’s lost territory was reclaimed. This territorial punishment had no effect whatsoever on avoiding a second WW, so it was a failure. Additionally, the inability of hte TOV to give Italy land it was promised led to Mussolini’s invasion of Abyssinia along with his use of chemical weapons on the defenceless populace. Mussolini’s policies demanded expansion and the inability of hte TOV or other treaties to acknowledge that was a failure. Similarly, after WW2, the splitting of East Germany and West Germany saw the coming of the Cold War. It was a mistake of peacemaking to put two contrasting ideologies of communism and capitalism in such close proximity to each other. More importantly, the rivalry between East and West Berlin caused tensions that broke into the Cold war as people in East Germany wanted to cross over to West Germany in order to experience capitalism. Another failure of peacemaking after WW2 was the social effects of the Indian partition 1947. The splitting of the country in half saw the genocide of Sikhs and Muslims at the borders as ghost trains full of corpses would transport Sikhs to India and Muslims to Pakistan, This rivalry between the nations continued toa full war over the independent state of Kashmir in 1948. As bot India and Pakistan were interested in capturing the country, leading to 250000 men dying in the conflict. It was a social mistake to turn the self-interest of one country into the greed of 2, and innocent men paid the price with their lives. Therefore, the partition of 1947 was mostly a social failure as the Indian nation was divided into 2. Both the peacemaking after WW1 nad WW2 were failures because millions of innocent people were killed and was were started. 

# In conclusion, although peacemaking after both WW1 and WW2 was a failure in temrs of territory. Peacemaking after WW2 was more successful overall than after WW1 because it led to economic prosperity. 
# """
# rubric_criteria = """Marks Level descriptor
# 0 Answers do not reach a standard described by the descriptors below.
# 1–3 There is little understanding of the demands of the question. The response is poorly structured or, where
# there is a recognizable essay structure, there is minimal focus on the task. Little knowledge of the world
# history topic is present. The student identifies examples to discuss, but these examples are factually
# incorrect, irrelevant or vague. The response contains little or no critical analysis. The response may consist
# mostly of generalizations and poorly substantiated assertions.
# 4–6 The response indicates some understanding of the demands of the question. While there may be an attempt
# to follow a structured approach, the response lacks clarity and coherence. Knowledge of the world history
# topic is demonstrated, but lacks accuracy and relevance. There is a superficial understanding of historical
# context. The student identifies specific examples to discuss, but these examples are vague or lack
# relevance. There is some limited analysis, but the response is primarily narrative/ descriptive in nature
# rather than analytical.
# 7–9 The response indicates an understanding of the demands of the question, but these demands are only
# partially addressed. There is an attempt to follow a structured approach. Knowledge of the world history
# topic is mostly accurate and relevant. Events are generally placed in their historical context. The examples
# that the student chooses to discuss are appropriate and relevant. The response makes links and/or
# comparisons (as appropriate to the question). The response moves beyond description to include some
# analysis or critical commentary, but this is not sustained.
# 10–12 The demands of the question are understood and addressed. Responses are generally well structured and
# organized, although there is some repetition or lack of clarity in places. Knowledge of the world history
# topic is mostly accurate and relevant. Events are placed in their historical context, and there is some
# understanding of historical concepts. The examples that the student chooses to discuss are appropriate and
# relevant, and are used to support the analysis/evaluation. The response makes effective links and/or
# comparisons (as appropriate to the question). The response contains critical analysis, which is mainly clear
# and coherent. There is some awareness and evaluation of different perspectives. Most of the main points
# are substantiated and the response argues to a consistent conclusion.
# 13–15 Responses are clearly focused, showing a high degree of awareness of the demands and implications of the
# question. Responses are well structured and effectively organized. Knowledge of the world history topic is
# accurate and relevant. Events are placed in their historical context, and there is a clear understanding of
# historical concepts. The examples that the student chooses to discuss are appropriate and relevant, and are
# used effectively to support the analysis/evaluation. The response makes effective links and/or comparisons
# (as appropriate to the question). The response contains clear and coherent critical analysis. There is
# evaluation of different perspectives, and this evaluation is integrated effectively into the answer. All, or
# nearly all, of the main points are substantiated, and the response argues to a consistent conclusion."""

# dave = DaveBot()
# feedback_dict_sentences = dave.get_feedback(student_writing, rubric_criteria)

# print(feedback_dict_sentences)