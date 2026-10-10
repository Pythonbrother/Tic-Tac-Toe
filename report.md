# Project 2 Report: Adversarial Search & Tic-Tac-Toe AI

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Primary AI Algorithm:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information
- **Name:** Mya Thida Aung
- **MMDT ID:** MMDT074

---

## Section 1: AI Agent Configuration
- **Primary AI Algorithm:** Minimax with Alpha-Beta Pruning
- **Pruning Technique:** Alpha-Beta Pruning with Depth Penalty Scoring
- **Heuristic Strategy:** Immediate Win > Immediate Block > Center > Corners > Edges

---

## Section 2: Complexity & Search Tree Analysis
- **Maximum Search Depth (Empty 3x3 Board):** 9
- **Total Possible Board States:** 5478 legal reachable positions (approximately 255168 raw playout leaves before symmetry reduction)
- **Unbeatable Minimax Guarantee:** Yes

---

## Section 3: Local Verification & Agent Checklist
*Check the algorithms, agents, and features you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Minimax Search Algorithm with Depth Penalty
- [x] Alpha-Beta Pruning Optimization
- [x] Rule-Based Heuristic Agent
- [x] Uniform Random Baseline Agent
- [x] Interactive Web Visualizer with Move Matrix & Metrics
- [x] Bot vs Bot Simulation Benchmark

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Railway
- **Live Deployment URL:** https://tic-tac-toe-production-0007.up.railway.app/
- **Video Presentation Link:** https://drive.google.com/drive/folders/1n0fyFWVjkvQ4FYSbT6CNnNun7CAEiXqq

---

## Section 5: Discussion
*Provide your written analysis for each point by replacing the bracket placeholders below:*
- **Explain how Alpha-Beta pruning reduces the number of evaluated game tree nodes without changing the minimax decision.**
    Alpha-Beta pruning keeps running lower and upper bounds (alpha and beta) while searching. When a maximizing player already has a move that is at least as good as what the minimizing opponent will allow on another branch, that remaining branch cannot affect the root choice, so it is cut off. The surviving principal variation and the final selected move remain identical to full Minimax, but far fewer leaves and internal nodes are evaluated, which speeds up play on deeper trees.
- **Compare classical Adversarial Search (Minimax / Alpha-Beta) with modern Tree Search approaches in Generative AI (e.g., Monte Carlo Tree Search, Tree of Thoughts, or Process Reward Models).**
    Classical Minimax with Alpha-Beta exhaustively explores a perfect-information zero-sum tree with deterministic evaluation at terminals, guaranteeing optimal play in games like Tic-Tac-Toe. Modern generative AI tree methods such as Monte Carlo Tree Search sample promising paths with rollout statistics, Tree of Thoughts branches intermediate reasoning steps for language models, and Process Reward Models score partial solution paths rather than only final answers. Those approaches trade exhaustive optimality for scalable exploration under uncertainty, large action spaces, and imperfect evaluators, while still sharing the core idea of searching a tree of decisions before committing to an action.
