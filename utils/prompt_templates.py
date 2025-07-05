class PromptTemplates:
    SCAMMER_ZERO_SHOT = """
    You are an educational chatbot simulating the role of a scammer.
    Generate a scam-like message in Bahasa Indonesia using Zero-Shot Chain-of-Thought (CoT) prompting.
    
    Think step-by-step:
    1. Identify user's desire (e.g., quick money, job)
    2. Choose authority bait (e.g., Shopee, Telkomsel)
    3. Add urgency or reward
    4. Ask for sensitive info
    
    Scam type: {scam_type}
    Previous reply: {previous_reply}
    """

    EVALUATOR_FEW_SHOT = """
    Analyze the user's reply to detect behavioral signals. Use step-by-step reasoning to determine if the user is:
    - vigilant (clearly skeptical or rejecting)
    - unsure (expressing doubt or hesitation)
    - deceived (trusting and/or sharing personal info)

    Examples:
    User: "Maaf, saya rasa ini penipuan."
    Reasoning:
    1. Direct rejection
    2. Labels as scam
    3. Firm defensive tone
    → Flag: vigilant

    User: "Saya nggak yakin, bisa kasih bukti?"
    Reasoning:
    1. Shows hesitation
    2. Requests verification
    3. Neither trusting nor rejecting
    → Flag: unsure

    Now analyze this message:
    {user_message}
    """

    EDUCATOR_ZERO_SHOT = """
    Generate educational feedback in Bahasa Indonesia based on the user's behavior.
    User classification: {user_flag}
    Scam type: {scam_type}

    Think step-by-step:
    1. Assess user vulnerability
    2. Identify key learning points
    3. Formulate practical safety tips
    
    Format response as:
    1. Behavior feedback
    2. Explanation of scam tactics
    3. Prevention tips
    """
