// Log Command Component
import { useState } from 'react';
import { sendCommand } from '../api'; // Assume this function sends command to your bot

const LogCommand = () => {
  const [channel, setChannel] = useState('');

  const handleSubmit = () => {
    sendCommand('logs', { channel });
  };

  return (
    <div>
      <label>Channel:</label>
      <input type="text" value={channel} onChange={(e) => setChannel(e.target.value)} />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};