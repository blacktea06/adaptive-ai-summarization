class Human:
    PERSONALITY_PROFILES = {
    # MBTI Personality Types 
    "INTP": "Prefers concise, logical feedback with minimal emotional language. Values autonomy.",
    "ENFP": "Responds well to enthusiastic, encouraging feedback. Appreciates creativity and big-picture framing.",
    "ISTJ": "Wants clear, structured instructions. Prefers practical and realistic feedback.",
    "ESFJ": "Appreciates warm, supportive guidance and socially affirming messages.",
    "ENTJ": "Prefers strategic overviews and confident, goal-oriented directives.",
    "INFJ": "Responds best to insightful, meaningful feedback with long-term perspective. Dislikes superficiality.",
    "ESTP": "Prefers direct, action-oriented feedback with immediate practical applications.",
    "ISFP": "Wants gentle, personalized feedback with creative options. Avoids rigid structures.",
    "ENFJ": "Appreciates inspirational feedback that connects to human values and team impact.",
    "ISTP": "Prefers technical, hands-on feedback with minimal verbal explanation. Show don't tell.",
    "INTJ": "Wants logically precise feedback with strategic implications. Include data where possible.",
    "ESTJ": "Prefers efficient, no-nonsense feedback with clear timelines and deliverables.",
    "ISFJ": "Responds well to patient, detailed feedback with appreciation for their efforts.",
    "ENTP": "Enjoys innovative, thought-provoking feedback that presents alternative approaches.",
    }

    #Note to self: Mention later the inverse relationship between engagement and level of detail abstraction

    COGNITIVE_STATES = {
    # LOW ENGAGEMENT (1) — cognitive strain, dysfunction, disengagement
    "frustrated": 1,
    "distrusting_swarm": 1,
    "overwhelmed": 1,
    "fatigued": 1,
    "panic": 1,
    "burnout": 1,
    "shutdown_mode": 1,
    "emotionally_blocked": 1,
    "frozen_response": 1,
    "apathetic": 1,
    "mentally_exhausted": 1,
    "disengaged": 1,
    "confused": 1,

    # LOW-MODERATE ENGAGEMENT (2) — low attention, distracted, unfocused
    "distracted": 2,
    "bored": 2,
    "analysis_paralysis": 2,
    "mechanical_response": 2,
    "second_guessing": 2,
    "self_doubt": 2,
    "detached": 2,
    "task_avoidance": 2,
    "restless": 2,
    "mind_wandering": 2,
    "disinterested": 2,

    # MODERATE ENGAGEMENT (3) — average, baseline, neutral states
    "neutral": 3,
    "curious": 3,
    "autopilot": 3,
    "cautious": 3,
    "observation_mode": 3,
    "scanning": 3,
    "slightly_distracted": 3,
    "routine_focused": 3,
    "reflective": 3,
    "moderately_attentive": 3,

    # HIGH ENGAGEMENT (4) — active, goal-oriented, focused states
    "focused": 4,
    "adrenaline_rush": 4,
    "coordinating": 4,
    "trusting_swarm": 4,
    "goal_oriented": 4,
    "vigilant": 4,
    "solution_seeking": 4,
    "analytical": 4,
    "intense_curiosity": 4,
    "alert": 4,
    "mindful": 4,
    "determined": 4,

    # PEAK ENGAGEMENT (5) — highly focused, peak performance states
    "hyperfocused": 5,
    "flow_state": 5,
    "leader_mode": 5,
    "locked_in": 5,
    "situational_awareness": 5,
    "strategic_thinking": 5,
    "in_the_zone": 5,
    "fully_immersed": 5,
    "peak_performance": 5,
    "laser_focused": 5,
    }

    #Human object has personality type, cognitive state and personality profile
    def __init__(self, name, personality_type, cognitive_state):
        self.personality_type = personality_type
        self.name = name
        self.cognitive_state = cognitive_state
        self.personality_profile = self.PERSONALITY_PROFILES.get(personality_type)
    




