# ai_modeling_service

AI-powered service to generate ArchiMate 3.2 elements from business context.

## Features
- Accepts business goals, initiatives, KPIs, and architecture text
- Maps input to ArchiMate elements using prompt-based AI
- Stores and returns structured, traceable outputs
- Allows user feedback and refinement
- Rate-limits and logs all generations

## Endpoints
- `POST /ai_modeling/generate`: Generate ArchiMate elements from input
- `GET /ai_modeling/history/{user_id}`: View previous generations
- `POST /ai_modeling/feedback`: Submit feedback on suggestions

## API
See [API_REFERENCE.md](./API_REFERENCE.md)
