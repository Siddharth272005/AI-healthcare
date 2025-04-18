import React, { useState } from "react";
import "./InputForm.css";

export const InputForm = ({ onSubmit }) => {
  const [text, setText] = useState("");
  const [image, setImage] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ text, image });
  };

  return (
    <form onSubmit={handleSubmit} className="form_container">
      <textarea
        placeholder="Start chatting or enter symptoms..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="textarea"
      />
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImage(e.target.files[0])}
        className="image_input"
      />
      <button type="submit" className="submit_btn px-12 py-4 rounded-full bg-[#fefae0] font-bold text-black tracking-widest uppercase transform hover:scale-105 hover:bg-[#21e065] transition-colors duration-200">Submit</button>
    </form>
  );
};
