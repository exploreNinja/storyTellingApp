from flask import Flask, render_template, jsonify, request
import json
import os
import random

app = Flask(__name__)

# Load stories from the 'stories' directory
def load_stories():
    stories = {}
    for filename in os.listdir('stories'):
        if filename.endswith('.json'):
            with open(f'stories/{filename}') as f:
                story_id = filename.replace('.json', '')
                stories[story_id] = json.load(f)
    return stories

stories = load_stories()

# Route to display the homepage with list of available stories
@app.route('/')
def index():
    return render_template('index.html', stories=stories)

# Route to view a particular story
@app.route('/story/<story_id>')
def view_story(story_id):
    story = stories.get(story_id)
    if not story:
        return f"Story '{story_id}' not found", 404
    return render_template('story.html', story=story)

# Route for handling user choices and updating the story's state
@app.route('/choose/<story_id>/<choice_id>')
def choose(story_id, choice_id):
    story = stories.get(story_id)
    if not story:
        return f"Story '{story_id}' not found", 404
    
    choice = story.get('choices', {}).get(choice_id)
    if not choice:
        return f"Choice '{choice_id}' not found for story '{story_id}'", 404
    
    next_sections = choice.get('next')
    section_texts = [story.get('sections', {}).get(section, 'No text available for this section.') for section in next_sections]
    
    # Randomize the order of the next sections to display
    random.shuffle(section_texts)
    
    return jsonify({
        "next_sections": next_sections,
        "text": section_texts
    })

if __name__ == '__main__':
    app.run(debug=True)
