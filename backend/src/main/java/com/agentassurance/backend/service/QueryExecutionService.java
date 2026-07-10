package com.agentassurance.backend.service;

import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class QueryExecutionService {

    // Mock data : correspond au schéma mock utilisé côté Python (users: id, name, email).
    // Sert à tester tout le pipeline sans avoir besoin d'une vraie base connectée.
    private final List<Map<String, Object>> mockUsers = List.of(
            Map.of("id", 1, "name", "Amine", "email", "amine@example.com"),
            Map.of("id", 2, "name", "Sara", "email", "sara@example.com"),
            Map.of("id", 3, "name", "Youssef", "email", "youssef@example.com")
    );

    /**
     * ⚠️ Version simplifiée : ne fait pas de vrai parsing SQL, retourne
     * toujours l'ensemble des mock data.
     *
     * Prochaine étape (avec PostgreSQL branché) : remplacer ceci par un vrai
     * appel JdbcTemplate.queryForList(sql) qui exécute le SQL pour de vrai.
     */
    public List<Map<String, Object>> execute(String sql) {
        return mockUsers;
    }
}
