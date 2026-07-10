package com.agentassurance.backend.dto;

import java.util.List;
import java.util.Map;

// Ce que le frontend (HTML) reçoit au final :
// - sql : la requête générée (null si erreur)
// - results : les données "exécutées" (mock pour l'instant)
// - error : message si les guardrails ont rejeté la requête (null si succès)
public record AskResponse(String sql, List<Map<String, Object>> results, String error) {
}
