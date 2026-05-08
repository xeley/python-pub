# Specification: Object Detection and Tracking

> This file is the authoritative specification for the project.
> It is written in Gherkin (BDD) and contains enough detail to regenerate the project from scratch.
> See [README.md](README.md) for setup and usage instructions.

---

## Architecture Constraint

All code must follow the **IOSP (Integration Operation Segregation Principle)**:

- **Operation** — contains `if`/loops/decisions; calls only stdlib/cv2/numpy; must be pure and testable.
- **Integration** — a flat, linear sequence of calls to Operations and other Integrations; zero branching.
- **Adapter** — thin I/O wrapper at the system boundary (camera, model, display).
- **Data** — immutable, typed value objects with no behaviour.

---

## Feature: Real-time object detection and annotation via camera feed

  As a user
  I want the camera system to detect objects in real time
  So that each detected object is highlighted with a labelled, coloured rectangular boundary

  Background:
    Given the camera is connected and active
    And the object detection service is running
    And the video stream is available

  ---

  ### Detection

  Scenario: Detect a single moving object
    Given a moving object enters the camera frame
    When the system processes the video stream
    Then the moving object should be detected
    And a rectangular boundary should be drawn around the moving object
    And the boundary should follow the object's movement

  Scenario: Detect multiple moving objects
    Given multiple moving objects are visible in the camera frame
    When the system processes the video stream
    Then each moving object should be detected
    And a separate rectangular boundary should be drawn around each moving object

  Scenario: Detect objects of different sizes
    Given a <object_size> object is visible in the camera frame
    When the system processes the video stream
    Then the object should be detected
    And a rectangular boundary should be drawn around the object

    Examples:
      | object_size |
      | small       |
      | medium      |
      | large       |

  Scenario: Real-time boundary updates
    Given a moving object changes position continuously
    When the system processes consecutive video frames
    Then the rectangular boundary coordinates should update in real time
    And the boundary should remain aligned with the object

  Scenario: Object exits the frame
    Given a moving object is detected in the camera frame
    When the object exits the camera frame
    Then the rectangular boundary should be removed

  Scenario: Detect objects under low light conditions
    Given an object is present in low light conditions
    When the system processes the video stream
    Then the object should still be detected
    And a rectangular boundary should be drawn around the object

  ---

  ### Classification and Labelling

  Scenario: Detected object is labelled with its class name
    Given an object is detected in the camera frame
    When the system processes the video stream
    Then the class name of the object (e.g. "person", "cat", "dog") should be displayed
    And the label should appear above the bounding box

  Scenario: Each class is rendered in a consistent colour
    Given objects of different classes are visible in the camera frame
    When the system processes the video stream
    Then each class should be assigned a unique colour
    And the same class should always render in the same colour across frames

  Scenario: Low-confidence detections are suppressed
    Given an object is partially visible or ambiguous
    When the system processes the video stream
    And the detection confidence is below the configured threshold
    Then no bounding box or label should be drawn for that object

  Scenario: Confidence threshold is configurable
    Given the user sets a custom confidence threshold in DetectionConfig
    When the system processes the video stream
    Then only detections at or above that threshold should be displayed

  ---

  ### Display and UI

  Scenario: FPS counter is shown on the frame
    Given the detection loop is running
    When each frame is rendered
    Then a frames-per-second counter should be visible in the top-right corner of the window
    And it should update every frame

  Scenario: Key hints are shown on the frame
    Given the detection loop is running
    When each frame is rendered
    Then a key hints bar should be visible in the bottom-left corner of the window
    And it should show "q  quit    r  reset size"

  Scenario: Window opens at default size
    Given the application starts
    When the detection window is created
    Then the window should open at 640×480 pixels by default

  Scenario: Window is resizable
    Given the detection window is open
    When the user drags the window border
    Then the window should resize freely to any size
    And the video feed should scale to fill the window

  Scenario: Window size can be reset via keyboard shortcut
    Given the user has resized the detection window
    When the user presses the "r" key
    Then the window should snap back to the default 640×480 size

  Scenario: Application quits via keyboard shortcut
    Given the detection window is open
    When the user presses the "q" key
    Then the application should exit cleanly
    And the camera and display resources should be released

  ---

  ### Error Handling

  Scenario: Camera feed unavailable at startup
    Given the camera is not connected or cannot be opened
    When the application starts
    Then the system should display a camera unavailable error message
    And the application should exit without crashing

  Scenario: Camera feed lost during operation
    Given the detection loop is running
    When the camera feed becomes unavailable mid-session
    Then the system should display a camera unavailable error message
    And the application should exit cleanly
    And camera and display resources should be released
