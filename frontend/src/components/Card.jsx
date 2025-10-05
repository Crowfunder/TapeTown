import React from "react";
import "./Card.css";

export default function Card({ title, description }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p>{description}</p>
      <button className="btn-secondary">Learn More</button>
    </div>
  );
}
