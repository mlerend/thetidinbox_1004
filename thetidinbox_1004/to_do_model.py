import spacy
import pandas as pd
from nltk.corpus import wordnet

def generate_to_do(text_input):
    # Load the pre-trained NER model
    nlp = spacy.load("en_core_web_sm")
    
    # Process the text input
    doc = nlp(text_input)
    
    # Extract named entities
    entities = [ent.text for ent in doc.ents]
    
    # Extract the person mentioned in the text
    person = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    
    # Extract the action verb in the text
    action_verb = [token.text for token in doc if token.pos_ == "VERB"]
    
    # To Do Generation
    if any(verb in action_verb for verb in ["provide", "update"]):
        if any(word in text_input for word in ["tasks", "task", "current tasks"]):
            to_do = "Provide updates on current tasks to {}".format(person[0]) if person else "Provide updates on current tasks"
        elif any(word in text_input for word in ["project", "current project"]):
            to_do = "Provide updates on the current project to {}".format(person[0]) if person else "Provide updates on the current project"
        elif any(word in text_input for word in ["status", "project status"]):
            to_do = "Update the project status"
        else:
            to_do = "Provide informations"
    elif any(verb in action_verb for verb in ["request", "provide"]):
        if "feedback" in text_input:
            to_do = "Provide feedback"
        elif any(word in text_input for word in ["approval", "approve"]):
            if any(word in text_input for word in ["purchase", "software license"]):
                to_do = "Approve a purchase requested by {}".format(person[0]) if person else "Approve purchases"
            elif any(word in text_input for word in ["training request", "training"]):
                to_do = "Approve {}'s training request".format(person[0]) if person else "Approve training requests"
            elif any(word in text_input for word in ["PTO request", "PTO"]):
                to_do = "Approve {}'s PTO request".format(person[0]) if person else "Approve PTO requests"
            elif any(word in text_input for word in ["payment request", "payment"]):
                to_do = "Approve {}'s payment request".format(person[0]) if person else "Approve payment requests"
        else:
            to_do = "Approve {}'s inputs".format(person[0])
    elif any(verb in action_verb for verb in ["confirm"]):
        if "delivery" in text_input:
            to_do = "Confirm a delivery from {}".format(person[0]) if person else "Confirm upcoming delivery"
        else:
            to_do = "Confirm {}'s request".format(person[0])
    elif any(verb in action_verb for verb in ["respond"]):
        if "customer inquiry" in text_input:
            to_do = "Respond to a customer inquiry submitted by {}".format(person[0]) if person else "Respond to a customer inquiry"
        else:
            to_do = "Get back to {}".format(person[0])
    elif any(verb in action_verb for verb in ["schedule", "appoint", "arrange", "organize", "plan", "programme"]):
        if any(word in text_input for word in ["call", "discuss", "meeting"]):
            to_do = "Schedule a meeting with {}".format(person[0]) if person else "Schedule upcoming meeting"
        elif "business trip" in text_input:
            to_do = "Schedule a business trip with {}".format(person[0]) if person else "Schedule upcoming business trip"
        elif "training" in text_input:
            to_do = "Schedule a training session for {}".format(person[0]) if person else "Schedule upcoming training session"
        elif any(word in text_input for word in ["business lunch", "lunch"]):
            to_do = "Schedule a business lunch with {}".format(person[0]) if person else "Schedule upcoming business lunch"
        else:
            to_do = "Schedule newt steps with {}".format(person[0])
    elif any(verb in action_verb for verb in ["accept"]):
        to_do = "Accept a meeting invitation from {}".format(person[0]) if person else "Accept meeting invitations"
    elif any(verb in action_verb for verb in ["prepare"]):
        to_do = "Prepare for the meeting with {}".format(person[0]) if person else "Prepare for the upcoming meeting"
    elif any(verb in action_verb for verb in ["postpone"]):
        to_do = "Postpone a meeting with {}".format(person[0]) if person else "Postpone the upcoming meeting"
    elif any(verb in action_verb for verb in ["send"]):
        if "reminder" in text_input:
            to_do = "Send a reminder for the upcoming meeting to {}".format(person[0]) if person else "Send a reminder for the upcoming meeting"
        else:
            to_do = "Double check {}'s meeting proposal".format(person[0])
    elif any(verb in action_verb for verb in ["join"]):
        if any(word in text_input for word in ["lunch"]):
            to_do = "Join {} for lunch".format(person[0]) if person else "Book lunch time"
        else:
            to_do = "Join {} for the upcoming meeting".format(person[0]) if person else "Attend upcoming meeting"
    
    elif any(verb in action_verb for verb in ["have", "discuss"]):
        to_do = "Set up a chat with {}".format(person[0])
    elif any(verb in action_verb for verb in ["provide"]):
        if "feedback" in text_input:
            to_do = "Provide feedback on the latest project report to {}".format(person[0]) if person else "Provide feedback on the latest project report"
        else:
            to_do = "Follow-up with {}"
    else:
        to_do = "No to do found"
    
    return to_do

