// Guild Profile Command Component
import { useState } from 'react';
import { sendCommand } from '../api'; // Assume this function sends command to your bot

const GuildProfileCommand = () => {
    const [channel, setChannel] = useState('');
    const [guildName, setGuildName] = useState('');
  
    const handleSubmit = () => {
      sendCommand('guild-profile', { channel, guildName });
    };
  
    return (
      <div>
        <label>Channel:</label>
        <input type="text" value={channel} onChange={(e) => setChannel(e.target.value)} />
        <label>Guild Name:</label>
        <input type="text" value={guildName} onChange={(e) => setGuildName(e.target.value)} />
        <button onClick={handleSubmit}>Submit</button>
      </div>
    );
  };
  