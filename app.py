from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
from werkzeug.serving import run_simple

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='pending')
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String(200)) 
    def __repr__(self):
        return f'<Todo {self.id}: {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'tags': self.tags.split(',') if self.tags else []
        }

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority', 'medium')
    due_date_str = request.form.get('due_date')
    tags = request.form.get('tags', '')
    
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            pass
    
    new_todo = Todo(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        tags=tags
    )
    
    db.session.add(new_todo)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_status/<int:id>/<string:status>')
def update_status(id, status):
    todo = Todo.query.get_or_404(id)
    todo.status = status
    db.session.commit()
    return redirect(url_for('index'))

# Enhanced features routes
@app.route('/enhanced-features')
def enhanced_features():
    todos = Todo.query.all()
    stats = {
        'total': len(todos),
        'completed': len([t for t in todos if t.status == 'completed']),
        'pending': len([t for t in todos if t.status == 'pending']),
        'high_priority': len([t for t in todos if t.priority == 'high']),
        'medium_priority': len([t for t in todos if t.priority == 'medium']),
        'low_priority': len([t for t in todos if t.priority == 'low'])
    }
    
    # Calculate completion percentage
    completion_percentage = 0
    if stats['total'] > 0:
        completion_percentage = round((stats['completed'] / stats['total']) * 100)
    
    return render_template('enhanced-features.html', todos=todos, stats=stats, completion_percentage=completion_percentage)

# API endpoints for enhanced features
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos/filter', methods=['GET'])
def filter_todos():
    status = request.args.get('status')
    priority = request.args.get('priority')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    search = request.args.get('search')
    
    query = Todo.query
    
    if status and status != 'all':
        query = query.filter(Todo.status == status)
    
    if priority and priority != 'all':
        query = query.filter(Todo.priority == priority)
    
    if from_date:
        try:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
            query = query.filter(Todo.due_date >= from_date_obj)
        except ValueError:
            pass
    
    if to_date:
        try:
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
            query = query.filter(Todo.due_date <= to_date_obj)
        except ValueError:
            pass
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Todo.title.like(search_term)) | 
            (Todo.description.like(search_term)) |
            (Todo.tags.like(search_term))
        )
    
    todos = query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos/export', methods=['GET'])
def export_todos():
    format_type = request.args.get('format', 'json')
    todos = Todo.query.all()
    
    if format_type == 'json':
        return jsonify([todo.to_dict() for todo in todos])
    elif format_type == 'csv':
        csv_data = "id,title,description,priority,status,due_date,created_at,tags\n"
        for todo in todos:
            todo_dict = todo.to_dict()
            tags_str = ','.join(todo_dict['tags']) if todo_dict['tags'] else ''
            csv_data += f"{todo.id},\"{todo.title}\",\"{todo.description}\",{todo.priority},{todo.status},{todo_dict['due_date']},{todo_dict['created_at']},\"{tags_str}\"\n"
        
        return csv_data, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=todos.csv'
        }
    
    return jsonify({'error': 'Invalid format'}), 400

@app.route('/api/stats', methods=['GET'])
def get_stats():
    todos = Todo.query.all()
    stats = {
        'total': len(todos),
        'completed': len([t for t in todos if t.status == 'completed']),
        'pending': len([t for t in todos if t.status == 'pending']),
        'high_priority': len([t for t in todos if t.priority == 'high']),
        'medium_priority': len([t for t in todos if t.priority == 'medium']),
        'low_priority': len([t for t in todos if t.priority == 'low'])
    }
    
    # Calculate completion percentage
    if stats['total'] > 0:
        stats['completion_percentage'] = round((stats['completed'] / stats['total']) * 100)
    else:
        stats['completion_percentage'] = 0
    
    return jsonify(stats)

if __name__ == '__main__':
    # Make the app available on your network
    host = '0.0.0.0'  # This makes the app accessible from any device on the network
    port = 5000
    
    print(f"Todo App is running on http://{host}:{port}")
    print("To access from other devices on your network, use your computer's IP address:")
    
    # Display your IP address for easy access from other devices
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"http://{ip_address}:{port}")
    
    # Run the app with debug mode enabled
    app.run(host=host, port=port, debug=True)