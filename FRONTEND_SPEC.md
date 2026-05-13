# FRONTEND_SPEC.md
# Frontend Component Specification

Component hierarchy, props, state management, and data flow for the multi-agent research assistant.

---

## Tech Stack

- **Framework:** Expo SDK 52+ with Expo Router (React Native for iOS, Android, Web)
- **Language:** TypeScript (strict mode)
- **Styling:** NativeWind (Tailwind CSS for React Native)
- **State:** React hooks (useState, useReducer) + Server-Sent Events (SSE)
- **Auth:** Supabase React Native SDK
- **Data fetching:** Native fetch + SSE streaming
- **Forms:** React Native forms with controlled components

---

## Page Structure (Expo Router)

```
app/
├── (tabs)/
│   ├── index.tsx             # ChatPage (main research interface)
│   ├── history.tsx           # HistoryPage (past research sessions)
│   └── settings.tsx          # SettingsPage (BYOK configuration)
│
├── auth/
│   ├── login.tsx             # LoginPage
│   ├── signup.tsx            # SignupPage
│   └── reset-password.tsx    # PasswordResetPage
│
├── _layout.tsx               # RootLayout (Supabase provider, fonts, tab navigation)
└── +not-found.tsx            # 404 page
```

**Note:** Expo Router uses file-based routing similar to Next.js App Router. The `(tabs)` group creates a tab navigator for the main app screens.

---

## Component Hierarchy

### Page: ChatPage (Main Research Interface)

```
<ChatPage>
  ├── <DashboardLayout>
  │   ├── <NavBar>
  │   │   ├── <Logo />
  │   │   ├── <UserMenu />
  │   │   └── <SettingsLink />
  │   │
  │   └── <MainContent>
  │       ├── <ChatPanel>         (Left column, 60% width)
  │       │   ├── <MessageList>
  │       │   │   ├── <UserMessage />
  │       │   │   │   └── text
  │       │   │   ├── <AIMessage>
  │       │   │   │   ├── <StreamingText />
  │       │   │   │   ├── <CitationLink /> (multiple)
  │       │   │   │   └── <EvalBadge />
  │       │   │   └── <EmptyState />  (when no messages)
  │       │   │
  │       │   └── <QueryInput>
  │       │       ├── <Textarea />
  │       │       └── <SubmitButton />
  │       │
  │       ├── <AgentTimeline>     (Right column, 40% width on desktop, below chat on mobile)
  │       │   ├── <TimelineHeader />
  │       │   └── <AgentNode /> × 5
  │       │       ├── icon
  │       │       ├── name
  │       │       └── status badge (pending | active | completed)
  │       │
  │       └── <SourcePanel>       (Slide-over on click, fixed right sidebar on desktop)
  │           ├── <PanelHeader>
  │           │   ├── title
  │           │   └── <CloseButton />
  │           ├── <SourceContent>
  │           │   ├── chunk text
  │           │   └── metadata (file, page, relevance score)
  │           └── <SourceActions>
  │               └── <CopyButton />
```

---

## Component Specifications

### ChatPanel

**Purpose:** Main chat interface with message history and input  
**State:** `messages: Message[]`, `isStreaming: boolean`, `streamingContent: string`

```typescript
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  evalScores?: EvalScores;
  timestamp: Date;
}

interface Citation {
  number: number;        // [1], [2], etc.
  sourceId: string;      // UUID from sources table
  content: string;       // Chunk text
  metadata: {
    filename?: string;
    page?: number;
    relevanceScore: number;
  };
}

interface EvalScores {
  faithfulness: number;      // 0-1
  answerRelevancy: number;   // 0-1
  contextPrecision: number;  // 0-1
  status: 'evaluating' | 'completed';
}
```

**Props:**
```typescript
interface ChatPanelProps {
  onCitationClick: (citation: Citation) => void;  // Opens SourcePanel
}
```

**Key behaviors:**
- Auto-scroll to bottom on new message
- Disable input during streaming
- SSE connection for streaming responses
- Render citations as clickable superscripts `[1]`

---

### MessageList

**Purpose:** Scrollable container for message history

**Props:**
```typescript
interface MessageListProps {
  messages: Message[];
  streamingContent?: string;        // Active streaming text
  onCitationClick: (citation: Citation) => void;
}
```

**Rendering:**
- Map over `messages` array
- If `streamingContent` present, render `<StreamingText>` after last message
- Empty state if no messages: "Ask a research question to get started"

---

### AIMessage

**Purpose:** Display AI response with citations and eval scores

**Props:**
```typescript
interface AIMessageProps {
  content: string;
  citations: Citation[];
  evalScores?: EvalScores;
  onCitationClick: (citation: Citation) => void;
}
```

**Rendering:**
- Parse `content` for citation markers `[1]`, `[2]`
- Render as `<CitationLink>` components (clickable)
- Markdown support for formatted text (bold, lists, code blocks)
- `<EvalBadge>` below content (if evalScores present)

---

### StreamingText

**Purpose:** Render text with typing cursor during streaming

**Props:**
```typescript
interface StreamingTextProps {
  content: string;
  isStreaming: boolean;
}
```

**Rendering:**
- Display content with blinking cursor at end (if `isStreaming`)
- Cursor CSS: `@keyframes blink { 50% { opacity: 0; } }`

---

### CitationLink

**Purpose:** Clickable citation number that opens source panel

**Props:**
```typescript
interface CitationLinkProps {
  citation: Citation;
  onClick: () => void;
}
```

**Rendering:**
```html
<button class="citation-link" onClick={onClick}>
  [{citation.number}]
</button>
```

**Styling:**
- `font-family: monospace`
- `color: primary-600`
- `text-decoration: underline`
- `hover: primary-700`

---

### EvalBadge

**Purpose:** Display RAGAS eval scores below AI response

**Props:**
```typescript
interface EvalBadgeProps {
  scores: EvalScores;
}
```

**Rendering:**
- If `status === 'evaluating'`: Show "Evaluating..." with spinner
- If `status === 'completed'`:
  ```
  Faithfulness: 0.85 | Answer Relevancy: 0.78 | Context Precision: 0.72
  ```
- Color code by threshold: green (≥ threshold), yellow (< threshold but ≥ 0.5), red (< 0.5)

---

### QueryInput

**Purpose:** Textarea for user query with submit button

**Props:**
```typescript
interface QueryInputProps {
  onSubmit: (query: string) => void;
  isDisabled: boolean;  // True during streaming
}
```

**Behavior:**
- Auto-resize textarea (max 6 lines)
- Submit on Cmd/Ctrl+Enter
- Disable during `isStreaming`
- Clear input after submit

---

### AgentTimeline

**Purpose:** Vertical timeline showing agent pipeline status

**State:** `agentStates: AgentState[]`

```typescript
interface AgentState {
  name: 'Planner' | 'Retriever' | 'Critic' | 'Synthesizer' | 'Evaluator';
  status: 'pending' | 'active' | 'completed';
  startTime?: Date;
  endTime?: Date;
}
```

**Rendering:**
- Vertical list of `<AgentNode>` components
- Connecting lines between nodes (dashed if pending, solid if completed)
- Auto-update via SSE events from backend

---

### AgentNode

**Purpose:** Single agent status indicator

**Props:**
```typescript
interface AgentNodeProps {
  agent: AgentState;
}
```

**Rendering:**
```
[Icon] Agent Name
       ● Status badge
       Duration (if completed)
```

**Status badge colors:**
- Pending: neutral-300 (gray)
- Active: agent color + pulsing animation
- Completed: agent color (muted, 50% opacity)

**Icon mapping:**
- Planner: Lightbulb
- Retriever: Magnifying glass
- Critic: Shield check
- Synthesizer: Document text
- Evaluator: Chart bar

---

### SourcePanel

**Purpose:** Slide-over panel showing citation source detail

**State:** `isOpen: boolean`, `citation: Citation | null`

**Props:**
```typescript
interface SourcePanelProps {
  citation: Citation | null;
  isOpen: boolean;
  onClose: () => void;
}
```

**Rendering:**
- Fixed right sidebar (desktop, 320px width)
- Slide-over overlay (mobile/tablet)
- Close on Esc key or click outside
- Render citation content + metadata

---

### SettingsPage (BYOK)

**Purpose:** User settings for API key management

**Components:**
```
<SettingsPage>
  ├── <SettingsHeader />
  ├── <APIKeySection>
  │   ├── <ProviderSelector>  (Anthropic | OpenAI | OpenRouter)
  │   ├── <KeyInput>
  │   │   ├── type="password"
  │   │   └── show/hide toggle
  │   ├── <TestConnectionButton />
  │   └── <SaveButton />
  │
  └── <KeyList>            (Existing saved keys)
      └── <KeyItem> × N
          ├── provider icon
          ├── masked key (sk-...***abc)
          ├── status (active | inactive)
          └── <DeleteButton />
```

**State:**
```typescript
interface APIKey {
  id: string;
  provider: 'anthropic' | 'openai' | 'openrouter';
  maskedKey: string;      // "sk-...***abc"
  isActive: boolean;
  createdAt: Date;
}
```

**Behavior:**
- Encrypt key before sending to backend (`/api/keys` POST)
- Test connection before saving (hit provider's health endpoint)
- Only one active key per provider
- Delete requires confirmation modal

---

## Data Flow

### Query Submission Flow

```
1. User types query in <QueryInput>
2. onClick Submit → POST /api/research/stream
3. Backend establishes SSE connection
4. Frontend:
   - Create EventSource("/api/research/stream")
   - Listen for events:
     - "agent_status" → Update AgentTimeline
     - "content_chunk" → Append to streamingContent
     - "citation" → Add to citations array
     - "eval_scores" → Set evalScores (async, arrives later)
     - "done" → Close stream, add to messages

5. User clicks citation → Open SourcePanel with citation data
```

### SSE Event Schema

```typescript
// Event: agent_status
{
  agent: 'Planner' | 'Retriever' | 'Critic' | 'Synthesizer' | 'Evaluator',
  status: 'active' | 'completed',
  timestamp: ISO8601
}

// Event: content_chunk
{
  content: string  // Fragment of answer text
}

// Event: citation
{
  number: number,
  sourceId: string,
  content: string,
  metadata: {...}
}

// Event: eval_scores
{
  faithfulness: number,
  answerRelevancy: number,
  contextPrecision: number
}

// Event: done
{
  sessionId: string  // For history tracking
}
```

---

## State Management Strategy

### Local State (React hooks)
- Component-local UI state (isOpen, selected index, etc.)
- Form inputs (QueryInput, SettingsPage)

### Lifted State (ChatPage)
- `messages: Message[]` (shared between ChatPanel and MessageList)
- `currentCitation: Citation | null` (opens SourcePanel)
- `agentStates: AgentState[]` (AgentTimeline data)

### Server State (Supabase)
- User auth session (Supabase Auth context)
- Research history (fetched on HistoryPage load)
- API keys (fetched on SettingsPage load)

### No global state library needed
- App is single-page focused (ChatPage)
- Minimal cross-component state sharing
- React Context sufficient for auth + theme (if dark mode added)

---

## Error Handling

### SSE Connection Errors
```typescript
eventSource.onerror = (error) => {
  // Show toast: "Connection lost. Retrying..."
  // Auto-reconnect with exponential backoff (1s, 2s, 4s, max 10s)
};
```

### API Errors (non-streaming)
```typescript
try {
  const response = await fetch('/api/keys', {...});
  if (!response.ok) {
    throw new Error(await response.text());
  }
} catch (error) {
  // Show error toast with message
  // Log to console for debugging
}
```

### Validation Errors
- Client-side validation (empty query, invalid key format)
- Show inline error below input field
- Disable submit button until valid

---

## Performance Optimizations

### Code Splitting
- Auth pages lazy-loaded (not on critical path)
- SettingsPage lazy-loaded (accessed rarely)

### Memoization
- `React.memo()` on `<AgentNode>` (prevent re-render if status unchanged)
- `useMemo()` for citation parsing (parse `[1]` markers once)

### Virtual Scrolling (deferred)
- Not needed for v1.0 (history capped at 50 messages per session)
- Add if performance degrades with long conversations

---

## Testing Strategy

### Unit Tests (Vitest)
- `<CitationLink>` rendering and onClick
- `<EvalBadge>` color logic based on scores
- `<QueryInput>` validation and submit

### Component Tests (React Testing Library)
- `<ChatPanel>` message rendering
- `<AgentTimeline>` status updates
- `<SourcePanel>` open/close behavior

### E2E Tests (Playwright)
- Full query flow (input → streaming → citations → source panel)
- BYOK settings (add key → save → test connection)
- Auth flow (signup → login → protected route)

---

**Frontend spec established:** 2026-05-09  
**Next:** Wireframes for all screens
