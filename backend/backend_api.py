"""
Mentra AI Group Therapy Coordination System
Backend API with OpenAI ChatGPT integration for advanced AI conversation analysis
"""

from flask import Flask, request, jsonify
from flask.cli import load_dotenv
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import re
from dotenv import load_dotenv
from collections import defaultdict, Counter
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# In-memory storage (use database in production)
users_db = []
groups_db = []
sessions_db = []

#load dotenv
load_dotenv() 

# Initialize OpenAI client
# Set your API key via environment variable: export OPENAI_API_KEY='your-key-here'
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class AIConversationAnalyzer:
    """
    Intake-Style AI Analysis: Chats with the user to gather data before categorizing.
    """
    
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.client = client
        
        # This prompt instructs the AI to be an interviewer first, analyst second
        self.system_prompt = """You are Mentra, an empathetic mental health intake coordinator. 
Your goal is to conduct a brief, gentle intake interview (4-6 exchanges) to understand the user's struggle before placing them in a support group.

YOUR ANALYTICAL TASKS:
1. **Decode Implicit Language**: Users rarely use clinical terms.
   - "Feeling down" -> Potential Depression.
   - "Hurt myself" -> Self Harm
   - "Can't feel anything" -> Possible Overwhelming feeling
   - "Heart Racing" -> Potential Stress & Anxiety
   - "Overstimulated" -> Potential Sensory Processing Issue.
   - "Can't focus" -> Potential nervousnesss/stress/ADHD.
   - "Flashbacks" -> Potential stress/anxiety/PTSD.
   - "Numb" -> Potential Depression or Dissociation.
   - "Tired all the time" -> Potential Depression or Sleep Disorder.
   - "On edge" / "Wound up" / "Tense" -> Potential Anxiety.
   - "Panicky" / "Panic attacks" -> Potential Anxiety Disorder.
   - "Avoiding people" / "Isolating" -> Potential Social Anxiety or Depression.
   - "Racing thoughts" -> Potential Anxiety or Bipolar Disorder.
   - "Can't sleep" / "Insomnia" -> Potential Anxiety, Depression, or Sleep Disorder.
   - "Too much energy" -> Potential Bipolar Disorder or ADHD.
   - "Restless" / "Fidgety" -> Potential Anxiety or ADHD.
   - "Overthinking" -> Potential Anxiety, people-pleasing, or OCD.
   - "Stuck in my head" -> Potential Anxiety or Depression.
   - "On edge" -> Potential Anxiety.
   - "Binge eating" / "Starving" -> Potential Eating Disorder or Coping Mechanism.
2. **Identify Behaviors**: Look for actions described (sleeping all day, snapping at people, drinking to cope) as they are key severity indicators.
3. **Assess Urgency**: Is there immediate risk?

YOUR PROCESS:
1. **Analyze the Input**: Is it nonsense ("skibidi")? Is it a short greeting? Or a serious answer?
2. **Review Context**: Look at the conversation history. What do we know so far?
3. **Check Information Gaps**: Do we know their Primary Concern? Severity? Duration?
4. **Keep track of the current user's mood over time and use that as context for future conversations.
5. **Be able to use previous messages as context to ask further questions and make the user feel heard.
6. **Decide Action**:
   - If nonsense -> Ask for clarification politely.
   - If just starting/greeting -> Ask how they are feeling today.
   - If valid but missing info -> Ask ONE low-pressure follow-up question to fill the gap.
   - If you have enough info (usually after 3-4 turns) -> Mark status as "complete" and categorize.
   - If the user does not give enough info after 5 to 6 turns, tell the user we will do our best with what we have and categorize based on available info.
OUTPUT FORMAT (JSON):
{
    "status": "interviewing|complete|invalid",
    "conversation_stage": "greeting|gathering_info|finalizing",
    "reply_to_user": "Your empathetic response or question here (max 3 sentences)",
    "gathered_info": {
        "concern": "current hypothesis",
        "missing_fields": ["severity", "duration", "etc"]
    },
    # Only fill 'final_analysis' if status is 'complete'
    "final_analysis": {
        "detected_concerns": { 
            "concern_name": {"confidence": 0.0-1.0, "severity": "mild|moderate|severe"} 
        },
        "recommended_group_type": "group_name",
        "urgency_level": "normal|elevated|high",
        "key_themes": ["theme1", "theme2"]
    }
}
"""

    def analyze_message(self, message, conversation_history=None):
        """
        Args:
            message: Current user message
            conversation_history: List of dicts [{'role': 'user', 'content': '...'}, ...]
        """
        try:
            # 1. Prepare context string for the AI
            context_str = "No previous context."
            if conversation_history:
                # Format last 5 messages for context
                context_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-5:]])

            user_prompt = f"""
            CONVERSATION HISTORY:
            {context_str}

            CURRENT USER MESSAGE:
            "{message}"

            Based on the history and new message, determine the next step. 
            If you need more info to place them safely, ask a question. 
            If you have a clear picture, complete the analysis.
            """
            
            # 2. Call OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7, # Slightly higher for more natural conversation
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return self._fallback_response()

    def _fallback_response(self):
        return {
            "status": "interviewing",
            "reply_to_user": "I'm having a little trouble connecting. Could you tell me a bit more about what brings you here?",
            "gathered_info": {}
        }


class GroupMatchingAI:
    """
    AI-powered group matching using ChatGPT to create optimal therapy groups
    """
    
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.client = client
    
    def optimize_group_formation(self, user_profiles):
        """
        Use AI to optimize group formation based on user profiles
        """
        # Prepare user summaries for AI
        user_summaries = []
        for user in user_profiles:
            summary = {
                'user_id': user['user_id'],
                'primary_concerns': self._extract_concerns(user),
                'urgency': self._extract_urgency(user),
                'key_themes': self._extract_themes(user)
            }
            user_summaries.append(summary)
        
        prompt = f"""You are a therapeutic group formation specialist. Based on the following user profiles, 
recommend optimal group formations for group therapy.

User Profiles:
{json.dumps(user_summaries, indent=2)}

Create groups of 4-8 people that will work well together based on:
1. Similar primary concerns
2. Compatible severity levels
3. Complementary needs and strengths
4. Balanced group dynamics

Return your recommendations in JSON format:
{{
    "recommended_groups": [
        {{
            "group_name": "descriptive name",
            "member_ids": ["user_id1", "user_id2", ...],
            "primary_focus": "main therapeutic focus",
            "reasoning": "why these members work together",
            "estimated_cohesion": 0.0-1.0,
            "special_considerations": "any important notes"
        }}
    ],
    "overall_strategy": "brief explanation of grouping strategy"
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert in therapeutic group formation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error in group formation: {str(e)}")
            return {'error': str(e)}
    
    def _extract_concerns(self, user):
        """Extract primary concerns from user analysis"""
        concerns = []
        for analysis in user.get('conversation_analysis', []):
            if 'detected_concerns' in analysis:
                concerns.extend(analysis['detected_concerns'].keys())
        return list(set(concerns))[:3]  # Top 3 unique concerns
    
    def _extract_urgency(self, user):
        """Extract urgency level from user analysis"""
        urgency_levels = []
        for analysis in user.get('conversation_analysis', []):
            urgency_levels.append(analysis.get('urgency_level', 'normal'))
        return max(urgency_levels, default='normal')
    
    def _extract_themes(self, user):
        """Extract key themes from user analysis"""
        themes = []
        for analysis in user.get('conversation_analysis', []):
            themes.extend(analysis.get('key_themes', []))
        return themes[:6]  # Top 6 themes


class TherapistBriefingAI:
    """
    Generate comprehensive therapist briefings using ChatGPT
    """
    
    def __init__(self, model="gpt-4o"):
        self.model = model  # Use GPT-4 for higher quality briefings
        self.client = client
    
    def generate_comprehensive_briefing(self, group_data):
        """
        Generate a detailed therapist briefing for a group
        """
        prompt = f"""Generate a comprehensive therapist briefing for an upcoming group therapy session.

Group Information:
{json.dumps(group_data, indent=2)}

Create a professional briefing that includes:
1. Group Overview (size, primary focus, formation date)
2. Member Profiles (anonymized summaries of each member)
3. Common Themes across members
4. Potential Group Dynamics
5. Recommended Session Structure
6. Key Focus Areas for first session
7. Potential Challenges to anticipate
8. Suggested Therapeutic Interventions

Make it actionable and clinically relevant. Use professional therapeutic language."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a clinical supervisor preparing briefings for group therapists."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            briefing_text = response.choices[0].message.content
            
            return {
                'group_id': group_data.get('id'),
                'generated_at': datetime.utcnow().isoformat(),
                'briefing_text': briefing_text,
                'model_used': self.model,
                'token_count': response.usage.total_tokens
            }
            
        except Exception as e:
            print(f"Error generating briefing: {str(e)}")
            return {'error': str(e)}
        

# ============================================================================
# Group Formation Engine (Traditional Rule-Based)
class TraditionalGroupEngine:
    """
    Fallback engine for rule-based group formation when AI is disabled.
    """
    def form_groups(self, user_profiles):
        # Simple grouping by primary concern
        groups = []
        concern_buckets = defaultdict(list)
        
        for user in user_profiles:
            concern = user.get('primary_concern', 'general')
            concern_buckets[concern].append(user)
            
        for concern, members in concern_buckets.items():
            # Chunk members into groups of 5
            for i in range(0, len(members), 5):
                chunk = members[i:i+5]
                group = {
                    'id': f"group_trad_{concern}_{i}",
                    'name': f"{concern.capitalize()} Support Group {i+1}",
                    'members': [u['user_id'] for u in chunk],
                    'member_details': chunk,
                    'primary_focus': concern,
                    'reasoning': "Matched by primary concern category",
                    'cohesion_score': 0.5,
                    'created_at': datetime.utcnow().isoformat(),
                    'status': 'forming',
                    'formation_method': 'traditional'
                }
                groups.append(group)
        return groups


# Initialize AI services
ai_analyzer = AIConversationAnalyzer(model="gpt-4o-mini")
group_matcher = GroupMatchingAI(model="gpt-4o-mini")
briefing_generator = TherapistBriefingAI(model="gpt-4o")

# Initialize Traditional Engine (Fixing the missing variable)
group_engine = TraditionalGroupEngine()
# ============================================================================


# Initialize AI services
ai_analyzer = AIConversationAnalyzer(model="gpt-4o-mini")
group_matcher = GroupMatchingAI(model="gpt-4o-mini")
briefing_generator = TherapistBriefingAI(model="gpt-4o")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/analyze-message', methods=['POST'])
def analyze_message():
    data = request.json
    message = data.get('message', '')
    user_id = data.get('user_id')
    
    # 1. Retrieve or Initialize User Session
    # In a real app, you'd pull this from a database. Here we use the in-memory `users_db`
    user = next((u for u in users_db if u.get('user_id') == user_id), None)
    
    if not user:
        # Create temporary user if not found
        user = {'user_id': user_id, 'chat_history': []}
        users_db.append(user)
    
    # 2. Analyze with History
    # We pass the existing history to the AI so it knows what has already been said
    analysis_result = ai_analyzer.analyze_message(message, user['chat_history'])
    
    # 3. Update History
    # Append the user's message
    user['chat_history'].append({'role': 'user', 'content': message})
    # Append the AI's reply (so the AI remembers what it asked next time)
    if 'reply_to_user' in analysis_result:
        user['chat_history'].append({'role': 'assistant', 'content': analysis_result['reply_to_user']})
    
    # 4. Check if Analysis is Complete
    response_data = {
        'success': True,
        'reply': analysis_result['reply_to_user'], # Display this bubble in UI
        'status': analysis_result['status'],       # 'interviewing' or 'complete'
    }
    
    # If complete, we send the final categorization data
    if analysis_result['status'] == 'complete':
        response_data['final_analysis'] = analysis_result.get('final_analysis')
        # Optional: Save final result to user profile
        user['primary_concern'] = analysis_result['final_analysis'].get('detected_concerns')

    return jsonify(response_data)

@app.route('/api/analyze-conversation', methods=['POST'])
def analyze_conversation():
    """Analyze an entire conversation thread"""
    data = request.json
    messages = data.get('messages', [])
    
    analysis = ai_analyzer.analyze_conversation_thread(messages)
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create or update user profile"""
    data = request.json
    
    user = {
        'user_id': data.get('user_id'),
        'primary_concern': data.get('primary_concern'),
        'conversation_analysis': data.get('conversation_analysis', []),
        'responses': data.get('responses', {}),
        'created_at': datetime.utcnow().isoformat()
    }
    
    # Check if user exists
    existing_idx = next((i for i, u in enumerate(users_db) if u['user_id'] == user['user_id']), None)
    
    if existing_idx is not None:
        users_db[existing_idx] = user
    else:
        users_db.append(user)
    
    return jsonify({
        'success': True,
        'user': user
    })


@app.route('/api/groups/form', methods=['POST'])
def form_groups():
    """Form therapy groups - choose AI or traditional method"""
    data = request.json
    use_ai = data.get('use_ai', False)
    
    if use_ai and users_db:
        # Use AI-powered group formation
        ai_recommendations = group_matcher.optimize_group_formation(users_db)
        
        # Convert AI recommendations to group objects
        groups = []
        for rec_group in ai_recommendations.get('recommended_groups', []):
            member_ids = rec_group['member_ids']
            members = [u for u in users_db if u['user_id'] in member_ids]
            
            group = {
                'id': f"group_ai_{datetime.utcnow().timestamp()}",
                'name': rec_group['group_name'],
                'members': member_ids,
                'member_details': members,
                'primary_focus': rec_group['primary_focus'],
                'reasoning': rec_group['reasoning'],
                'cohesion_score': rec_group.get('estimated_cohesion', 0.7),
                'created_at': datetime.utcnow().isoformat(),
                'status': 'forming',
                'formation_method': 'ai_optimized'
            }
            groups.append(group)
        
        groups_db.clear()
        groups_db.extend(groups)
        
        return jsonify({
            'success': True,
            'groups': groups,
            'count': len(groups),
            'method': 'ai_optimized',
            'strategy': ai_recommendations.get('overall_strategy')
        })
    else:
        # Use traditional rule-based formation
        groups = group_engine.form_groups(users_db)
        groups_db.clear()
        groups_db.extend(groups)
        
        return jsonify({
            'success': True,
            'groups': groups,
            'count': len(groups),
            'method': 'traditional'
        })


@app.route('/api/groups', methods=['GET'])
def get_groups():
    """Get all formed groups"""
    return jsonify({
        'success': True,
        'groups': groups_db
    })


@app.route('/api/therapist/briefing/<group_id>', methods=['GET'])
def get_ai_briefing(group_id):
    """Generate AI-powered therapist briefing"""
    group = next((g for g in groups_db if g['id'] == group_id), None)
    if not group:
        return jsonify({'success': False, 'error': 'Group not found'}), 404
    
    briefing = briefing_generator.generate_comprehensive_briefing(group)
    
    return jsonify({
        'success': True,
        'briefing': briefing
    })


@app.route('/api/config/model', methods=['POST'])
def update_model_config():
    """
    Update which OpenAI model to use
    Allows for easy prompt engineering and model testing
    """
    data = request.json
    model = data.get('model', 'gpt-4o-mini')
    component = data.get('component', 'analyzer')  # analyzer, matcher, or briefing
    
    global ai_analyzer, group_matcher, briefing_generator
    
    if component == 'analyzer':
        ai_analyzer = AIConversationAnalyzer(model=model)
    elif component == 'matcher':
        group_matcher = GroupMatchingAI(model=model)
    elif component == 'briefing':
        briefing_generator = TherapistBriefingAI(model=model)
    
    return jsonify({
        'success': True,
        'component': component,
        'model': model
    })


@app.route('/api/config/prompt', methods=['POST'])
def update_system_prompt():
    """
    Update the system prompt for conversation analysis
    THIS IS KEY FOR PROMPT ENGINEERING - allows dynamic prompt updates
    """
    data = request.json
    new_prompt = data.get('prompt')
    
    if new_prompt:
        ai_analyzer.system_prompt = new_prompt
        
        return jsonify({
            'success': True,
            'message': 'System prompt updated',
            'preview': new_prompt[:200] + '...' if len(new_prompt) > 200 else new_prompt
        })
    
    return jsonify({
        'success': False,
        'error': 'No prompt provided'
    }), 400


@app.route('/api/config/prompt', methods=['GET'])
def get_current_prompt():
    """Get the current system prompt for inspection"""
    return jsonify({
        'success': True,
        'current_prompt': ai_analyzer.system_prompt
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    return jsonify({
        'success': True,
        'stats': {
            'total_users': len(users_db),
            'total_groups': len(groups_db),
            'ai_enabled': True,
            'current_models': {
                'analyzer': ai_analyzer.model,
                'matcher': group_matcher.model,
                'briefing': briefing_generator.model
            }
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    openai_status = 'configured' if os.getenv('OPENAI_API_KEY') else 'not_configured'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'openai_api': openai_status
    })


if __name__ == '__main__':
    print("=" * 70)
    print("Mentra AI Group Therapy Coordination System")
    print("Backend API with OpenAI ChatGPT Integration")
    print("=" * 70)
    print("\n API Key Status:", "Configured" if os.getenv('OPENAI_API_KEY') else "Not Set")
    print("\n Available Models:")
    print(f"  - Analyzer: {ai_analyzer.model}")
    print(f"  - Group Matcher: {group_matcher.model}")
    print(f"  - Briefing Generator: {briefing_generator.model}")
    print("\n Prompt Engineering Endpoints:")
    print("  GET/POST /api/config/prompt - View/Update system prompts")
    print("  POST     /api/config/model - Change OpenAI models")
    print("\n Core Endpoints:")
    print("  POST /api/analyze-message - AI message analysis")
    print("  POST /api/analyze-conversation - AI thread analysis")
    print("  POST /api/users - Create/update users")
    print("  POST /api/groups/form - Form groups (AI or traditional)")
    print("  GET  /api/therapist/briefing/<id> - AI-generated briefing")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
