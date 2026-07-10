package com.agentassurance.backend.dto;

// Un "record" Java = une classe simple qui ne fait que transporter des données.
// Équivalent d'un dict Python {"question": "..."} mais typé.
public record QuestionRequest(String question) {
}
