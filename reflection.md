# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
Upon initial readings, it seems that we need an owner that can contain multiple pets, and those pets have multilpe tasks that need to be completed.
- What classes did you include, and what responsibilities did you assign to each?
Pet, Task, Scheduler, and owner

Pet: Name, Age, Owner_Name, Add Pet, Tasks
Task: Duration, Priority, Pull/Add Tasks

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Time availability to maximize efficiency, urgency to alter priority
- How did you decide which constraints mattered most?
Time availability; logically, without time, you can't get anything done
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
overlapping times/tasks
- Why is that tradeoff reasonable for this scenario?
It's possible to do 2 jobs at once such as walking 2 dogs together rather than each seperately.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
