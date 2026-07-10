package com.agentassurance.backend.controller;

import com.agentassurance.backend.dto.AskResponse;
import com.agentassurance.backend.dto.PythonSqlResponse;
import com.agentassurance.backend.dto.QuestionRequest;
import com.agentassurance.backend.service.QueryExecutionService;
import com.agentassurance.backend.service.SqlGenerationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*") // autorise le frontend (autre port/origine) à appeler cette API
public class SqlController {

    private final SqlGenerationService sqlGenerationService;
    private final QueryExecutionService queryExecutionService;

    public SqlController(SqlGenerationService sqlGenerationService,
                          QueryExecutionService queryExecutionService) {
        this.sqlGenerationService = sqlGenerationService;
        this.queryExecutionService = queryExecutionService;
    }

    @PostMapping("/ask")
    public ResponseEntity<AskResponse> ask(@RequestBody QuestionRequest request) {

        // Étape 1 : demander le SQL à l'API Python (Mistral + guardrails)
        PythonSqlResponse pythonResponse = sqlGenerationService.generateSql(request.question());

        if (pythonResponse.error() != null) {
            // Guardrails ont rejeté, ou la question était invalide
            return ResponseEntity.badRequest()
                    .body(new AskResponse(null, null, pythonResponse.error()));
        }

        // Étape 2 : "exécuter" le SQL (mock data pour l'instant)
        List<java.util.Map<String, Object>> results = queryExecutionService.execute(pythonResponse.sql());

        return ResponseEntity.ok(new AskResponse(pythonResponse.sql(), results, null));
    }
}
