package com.agentassurance.backend.dto;

// Représente ce que renvoie ton API Python : soit {"sql": "..."} soit {"error": "..."}
// Un seul des deux champs est rempli à la fois.
public record PythonSqlResponse(String sql, String error) {
}
