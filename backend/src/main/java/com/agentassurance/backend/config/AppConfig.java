package com.agentassurance.backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class AppConfig {

    // RestTemplate = l'outil Spring pour appeler d'autres API HTTP,
    // ici il servira à appeler ton API Python (Flask).
    // Équivalent Python : la librairie "requests".
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
