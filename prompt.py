check_prompts = {
    "Task": "Please identify if the following paper is related to the topic of large language models (LLMs) or involves the use of LLMs based on the following provided information.\n",
    "Input": "Paper Title: {title}\nAbstract (if available): {abstract}\nTopics (if available): {topics}\n",
    "Instruction": "Guidance: If the abstract is unavailable, please use the title and topics to make your determination. Please note that a paper mentioning concepts like 'neural network', 'machine learning', 'artificial intelligence', or any NLP tasks always suggests a connection to LLMs. For example, a paper titled 'The improved neural network model in humor detection' is very likely to involve LLMs. Respond 'Yes' for such papers.",
    "Output": "Please only respond with either 'Yes' or 'No'. Please do not return other output.\n"
}

discipline_prompts = {
    "Task": "Please extract the discipline-related information from the following author's affiliation: {affiliation}\n",
    "Instruction": "For example, for 'Department of Biological Science, Joseph Ayo Babalola University, Nigeria', return 'Biological Science'. If it is not written in English, translate it to English and return. If you cannot identify any discipline-related information, return 'None'. Please do not return other output or explanation. \n"
}


def create_check_prompt(row):
    """Create prompts for LLM inputs to check if a paper is related to LLM topics"""
    title = row['title']
    abstract = row['abstract']
    topics = row['topics.display_name']
    if isinstance(abstract, str):
        words = abstract.split()
        if len(words) > 300:
            abstract = ' '.join(words[:300])
    else:
        abstract = "N/A"
    prompt = check_prompts["Task"] + check_prompts["Input"].format(title=title, abstract=abstract, topics=topics) + check_prompts['Instruction'] + check_prompts["Output"]
    return prompt


def create_discipline_prompt(row):
    """Create prompts for LLM inputs to extract discipline information."""
    raw_affiliation = row['raw_affiliation']
    prompt = discipline_prompts["Task"].format(affiliation=raw_affiliation) + discipline_prompts["Instruction"]
    return prompt