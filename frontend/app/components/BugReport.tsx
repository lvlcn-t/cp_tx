// Bug Report Command Component
import { useState } from 'react';
import { sendCommand } from '../api'; // Assume this function sends command to your bot

const BugReportCommand = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
  
    const handleSubmit = () => {
      sendCommand('bug', { title, description });
    };
  
    return (
      <div>
        <label>Title:</label>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
        <label>Description:</label>
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
        <button onClick={handleSubmit}>Submit</button>
      </div>
    );
  };