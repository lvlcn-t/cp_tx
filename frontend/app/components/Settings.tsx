// Settings Component
import { useState } from 'react';
import { sendCommand } from '../api'; // Assume this function sends command to your bot
import axios from 'axios';
import { Formik, Form } from 'formik';
import Dropdown from './Dropdown';
import Field from './Field';

const Settings = () => {
    const [region, setRegion] = useState('');
    const [server, setServer] = useState('');
    const [guildName, setGuildName] = useState('');
  
    const handleSubmit = () => {
      // update settings here.ExecutionEnvironment.BASE_PATH + "/api/bot-settings";
  
      // Submit handler
      const handleSubmit = async (values: BotSettings) => {
          try {
              await axios.post(apiPath, values);
              alert("Bot settings updated successfully!");
          } catch (err) {
              console.error(err);
              alert("Failed to update settings.");
          }
      };
  
      return (
          <Formik initialValues={initialValues} onSubmit={handleSubmit}>
              {({ isSubmitting }) => (
                  <Form>
                      <h2>Bot Settings</h2>
  
                      <Dropdown name="logsChannel" label="Logs Channel" options={channels} />
                      <Dropdown name="guildProfileChannel" label="Guild Profile Channel" options={channels} />
                      <Field name="guildName" label="Guild Name" />
  
                      <button type="submit" disabled={isSubmitting}>
                          Save
                      </button>
                  </Form>
              )}
          </Formik>
      );
  };
  