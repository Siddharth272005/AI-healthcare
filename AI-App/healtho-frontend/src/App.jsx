// src/App.jsx
import React, { useState } from "react";
import { InputForm } from "./components/InputForm";
import axios from "axios";
import "./App.css";
import { AuroraBackground } from "./components/AuroraBackground";

const App = () => {
  const [output, setOutput] = useState();

  const handleFormSubmit = async (data) => {
    const formData = new FormData();
    formData.append("text", data.text);
    if (data.image) {
      formData.append("image", data.image);
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/predict",
        formData
      );
      setOutput(JSON.stringify(response.data));
    } catch (error) {
      setOutput("Error occurred: " + error);
    }
  };

  return (
    <>
    <AuroraBackground>
      <div className="chat_container poppins-medium">
      <h1 className="poppins-bold">Healthcare App</h1>
      <InputForm onSubmit={handleFormSubmit} />
      <div>
        <p className="output_text">{output}</p>
      </div>
      </div>
      </AuroraBackground>
      </>
  );
};

export default App;
