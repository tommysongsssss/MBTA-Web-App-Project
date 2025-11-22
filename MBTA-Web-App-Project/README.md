# MBTA-Web-App-Project

This is the base repository for Web App project. Please read the [instructions](instructions.md) for details.

Team: Astrid Yuan & Thomas Song

### Project Writeup and Reflection

#### 1. Project Overview

Our project is a Flask-based web application designed to help users find the nearest MBTA station based on either a place name or geographic coordinates within the Greater Boston area. Using the Mapbox Geocoding API, the app converts user input into latitude and longitude, and then queries the MBTA v3 API to identify the closest station and whether it is wheelchair accessible. Beyond the core functionality, we implemented several “wow” features, including customized "Zhi Li MBTA search engine", real-time weather information from the OpenWeather API, U.S. holiday detection through the AbstractAPI Holidays service, a Mapbox static map preview, and an interactive zoomable Leaflet map that displays the station's exact location. The final app combines backend API logic, frontend visual components, and user-friendly interaction to deliver a clean, informative, and engaging experience.

#### 2. Reflection

1. **Development Process**. 

Breaking the project into small helper functions and testing each one early went well. Using main() to print API responses helped us quickly verify that Mapbox and MBTA were working before moving on to Flask. This prevented many later errors.

The biggest challenges were API errors and file-path issues. Each API had a different URL format and JSON structure, which caused frequent mistakes. We also struggled for a long time because our index.html was placed in the wrong folder, so Flask kept returning blank pages. Learning how strict Flask is about folder paths would have saved us a lot of time. Another challenge was the “use my current location” feature—we tried many times, but it consistently produced errors, so we eventually removed it. We also found that while the app works for common places like “Boston,” it struggles with specific inputs like “Babson College.”

Our problem-solving approach was iterative: whenever something failed, we checked the API URL, printed raw JSON, and isolated each helper function. AI tools helped us debug issues, generate the cover page, improve the CSS styling, and implement the interactive map.

If we were doing the project again, we would organize our file paths correctly from the start and commit changes to GitHub more consistently. Our collaboration slowed down at times because we didn’t push updates regularly, which meant waiting for each other’s changes. Eventually, we decided to work together in person and run everything from one laptop, which solved the syncing issues. Understanding Flask’s strict folder structure and maintaining better version control from the beginning would have made the entire development process much smoother.

    

2. **Teamwork & Work Division**.

We divided the project evenly. One team member focused more on the helper functions and API logic, while the other handled the Flask routes, HTML templates, and CSS. We also worked together on the “wow” features like the interactive map and the weather/holiday header.

Our original plan was to work separately and sync through GitHub, but inconsistent commits made it difficult to stay aligned. After running into repeated version-control issues, we switched to working together in person and developing from one laptop, which made debugging and testing much faster.

If we were doing the project again, we would push code more frequently, use clearer GitHub practices, and confirm the correct folder structure at the start. Better coordination and version control would have made collaboration smoother.


3. **Learning & Use of AI Tools**. 

This project helped us better understand how APIs and JSON data work in practice. By working with Mapbox, MBTA, OpenWeather, and the Holidays API, we learned how to read documentation, build correct URLs, and extract the values we needed from different JSON structures. We also gained a clearer understanding of Flask’s backend workflow—especially how routes, templates, and file paths connect—and how important project organization is for preventing errors.
Writing small helper functions taught us how useful modular design is. Testing each function in main() made debugging much easier and helped us isolate mistakes before integrating everything into the Flask app.

We used AI tools, mainly ChatGPT, for debugging, clarifying API behavior, generating CSS styles, improving code structure, and helping us implement the interactive Leaflet map as our “wow” feature. AI also helped us design the cover page and refine the overall layout. However, we learned that AI suggestions still need to be tested, since API formats don’t always match the examples.

If we were starting over, we would pay closer attention to folder structure and paths from the beginning—they caused many early errors—and we would document more as we went. Screenshots of JSON debugging, template errors, and our first working Flask form are included to show important points in our development process.

