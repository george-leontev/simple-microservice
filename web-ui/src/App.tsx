import { useEffect, useRef } from 'react';
import './App.css';
import axios from 'axios';
import { io } from 'socket.io-client';


function App() {
  const formRef = useRef<HTMLFormElement>(null);

  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const socket = io("http://localhost:8000", {
      transports: ['websocket']
    });
    socket.on("get_acknowledgement", (message: any) => {
      if (textAreaRef.current) {
        textAreaRef.current.value += `mail ${message.mail_uid} was send by service ${message.service_uid}\n\r`;
      }
    });

    return () => {
      socket.disconnect();
    }
  }, []);

  const handleInputChange = async () => {
    if (formRef.current) {
      const formData = new FormData(formRef.current);
      const mail = {} as any;
      Array.from(formData.keys()).forEach(key => {
        mail[key] = formData.get(key);
      });

      mail.uid = ''

      await axios.request({
        method: 'POST',
        data: mail,
        url: 'http://127.0.0.1:8000/mail-services'
      });
    }
  };

  return (
    <div className="App">
      <form className='mail-form' ref={formRef}>
        <div className='sender-input'>
          <label htmlFor="">From:</label>
          <input type="text" name='sender' value='me' />
        </div>

        <div className='reciever-input'>
          <label htmlFor="">To:</label>
          <input type="text" name='reciever' value='you' />
        </div>

        <div className='message-input'>
          <label htmlFor="">Message:</label>
          <input type="text" name='message' value='hi world' />
        </div>
      </form>

      <div className='navbar'>
        <button onClick={handleInputChange}>SEND</button>
      </div>

      <div>
        <textarea style={{ width: 400, height: 200 }} ref={textAreaRef}></textarea>
      </div>

    </div>
  );
}

export default App;
