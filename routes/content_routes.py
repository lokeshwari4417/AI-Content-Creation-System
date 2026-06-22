# ============================================================
# routes/content_routes.py - Flask Blueprint
# Updated to use Google Gemini API (Free)
# ============================================================

import os
from flask import (
    Blueprint, render_template, request,
    jsonify, send_file, abort
)
import google.generativeai as genai
from models.content_model import db, ContentHistory
from prompts.prompt_templates import build_prompt
import io

# ── Blueprint Definition ─────────────────────────────────────
content_bp = Blueprint('content', __name__)


def get_gemini_model():
    """
    Configures and returns a Gemini GenerativeModel instance.
    Returns None if API key is missing.
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'AIzaSy_your_actual_key_here':
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')


# ── HOME PAGE ────────────────────────────────────────────────
@content_bp.route('/')
def index():
    return render_template('index.html')


# ── GENERATE CONTENT ─────────────────────────────────────────
@content_bp.route('/generate', methods=['POST'])
def generate_content():
    data = request.get_json()

    # ── Input Validation ─────────────────────────────────────
    required_fields = ['content_type', 'topic', 'audience', 'tone', 'length']
    for field in required_fields:
        if not data.get(field, '').strip():
            return jsonify({
                'success': False,
                'error': f'"{field.replace("_", " ").title()}" field is required.'
            }), 400

    content_type = data['content_type'].strip()
    topic        = data['topic'].strip()
    audience     = data['audience'].strip()
    tone         = data['tone'].strip()
    length       = data['length'].strip()

    # ── Build Prompt ─────────────────────────────────────────
    prompt = build_prompt(content_type, topic, audience, tone, length)

    # ── Call Gemini API ──────────────────────────────────────
    model = get_gemini_model()

    if model is None:
        # Demo mode — no API key configured
        generated_text = _demo_content(content_type, topic, audience, tone)
    else:
        try:
            response = model.generate_content(prompt)
            generated_text = response.text.strip()

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Gemini API error: {str(e)}'
            }), 502

    # ── Save to Database ─────────────────────────────────────
    record = None
    try:
        record = ContentHistory(
            content_type=content_type,
            topic=topic,
            audience=audience,
            tone=tone,
            length=length,
            generated_content=generated_text,
        )
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        print(f"⚠️  Database save error: {e}")

    return jsonify({
        'success': True,
        'content': generated_text,
        'record_id': record.id if record else None,
        'prompt_used': prompt
    })


# ── HISTORY PAGE ─────────────────────────────────────────────
@content_bp.route('/history')
def history():
    search_query = request.args.get('search', '').strip()

    if search_query:
        records = (
            ContentHistory.query
            .filter(ContentHistory.topic.ilike(f'%{search_query}%'))
            .order_by(ContentHistory.created_at.desc())
            .all()
        )
    else:
        records = (
            ContentHistory.query
            .order_by(ContentHistory.created_at.desc())
            .all()
        )

    return render_template('history.html', records=records, search=search_query)


# ── DELETE RECORD ─────────────────────────────────────────────
@content_bp.route('/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = ContentHistory.query.get(record_id)
    if not record:
        return jsonify({'success': False, 'error': 'Record not found.'}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Record deleted successfully.'})


# ── EXPORT AS TXT ─────────────────────────────────────────────
@content_bp.route('/export/<int:record_id>')
def export_txt(record_id):
    record = ContentHistory.query.get(record_id)
    if not record:
        abort(404)

    file_content = (
        f"AI Content Creation System — Export\n"
        f"{'=' * 50}\n\n"
        f"Content Type : {record.content_type}\n"
        f"Topic        : {record.topic}\n"
        f"Audience     : {record.audience}\n"
        f"Tone         : {record.tone}\n"
        f"Length       : {record.length}\n"
        f"Generated At : {record.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"{'=' * 50}\n\n"
        f"{record.generated_content}\n"
    )

    buffer = io.BytesIO(file_content.encode('utf-8'))
    buffer.seek(0)

    safe_topic = ''.join(c if c.isalnum() else '_' for c in record.topic[:30])
    filename = f"{record.content_type.replace(' ', '_')}_{safe_topic}.txt"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )


# ── DEMO CONTENT ──────────────────────────────────────────────
def _demo_content(content_type, topic, audience, tone):
    return (
        f"⚠️  DEMO MODE — No Gemini API key detected.\n\n"
        f"This is a sample {content_type} about \"{topic}\" for {audience} "
        f"in a {tone} tone.\n\n"
        f"To generate real AI content:\n"
        f"1. Go to aistudio.google.com\n"
        f"2. Get a free API key\n"
        f"3. Add it to your .env as GEMINI_API_KEY\n"
        f"4. Restart the Flask server\n\n"
        f"Topic     : {topic}\n"
        f"Audience  : {audience}\n"
        f"Tone      : {tone}"
    )