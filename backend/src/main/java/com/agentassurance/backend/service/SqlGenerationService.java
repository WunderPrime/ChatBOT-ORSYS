package com.agentassurance.backend.service;

import com.agentassurance.backend.dto.PythonSqlResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class SqlGenerationService {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper();

    // Lu depuis application.properties : python.api.url=http://localhost:5001/api/generate-sql
    @Value("${python.api.url}")
    private String pythonApiUrl;

    public SqlGenerationService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    /**
     * Appelle l'API Python (Mistral + guardrails) pour transformer
     * une question en langage naturel en requête SQL.
     */
    public PythonSqlResponse generateSql(String question) {
        Map<String, String> body = Map.of("question", question);

        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(pythonApiUrl, body, Map.class);
            Map<?, ?> data = response.getBody();
            String sql = data != null ? (String) data.get("sql") : null;
            return new PythonSqlResponse(sql, null);

        } catch (HttpClientErrorException e) {
            // L'API Python répond avec un code 400 quand les guardrails rejettent le SQL.
            // On récupère le message d'erreur dans le corps de la réponse.
            String errorMessage = extractErrorMessage(e.getResponseBodyAsString());
            return new PythonSqlResponse(null, errorMessage);

        } catch (Exception e) {
            // Ex: le service Python n'est pas démarré, mauvaise URL, timeout...
            return new PythonSqlResponse(null, "Impossible de contacter le service Python : " + e.getMessage());
        }
    }

    private String extractErrorMessage(String jsonBody) {
        try {
            Map<?, ?> map = objectMapper.readValue(jsonBody, Map.class);
            Object error = map.get("error");
            return error != null ? error.toString() : "Erreur inconnue renvoyée par le service Python.";
        } catch (Exception ex) {
            return "Erreur inconnue renvoyée par le service Python.";
        }
    }
}
