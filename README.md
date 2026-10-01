# CONTEXT-AWARE-PROACTIVE-NETWORK-SELECTION-A-REINFORCEMENT-LEARNING-FRAMEWORK-FOR-OPTIMISING-MOBILE
This project introduces a Context-Aware Network Selection System that proactively  and intelligently suggests the best network to a user according to real-time contextual  information. 
## 🎥 Project Demo

[Watch the Project Demo on YouTube](https://youtu.be/DWQ_oWB4xDI)
##  Automated API Load Testing & Performance Analytics 
[watch the demo on youtube](https://youtu.be/eFfldI0EHNE)
## Enterprise Dataset Expansion & Advanced Feature Synthesis
[watch the demo on youtube](https://youtu.be/zYqCfl24oJg)
## Podman Deployment Demonstration
[watch the demo on youtube](https://youtu.be/AsjGI_re1xw)


1. Data Collection
The system starts with historical/synthesized mobile network records containing device, geographical, temporal, carrier, and network-context information. The raw data is stored as CSV and processed using Pandas.

2. Original / Old Columns
The original dataset columns used as the base data are: Device ID, Latitude, Longitude, Epoch Timestamp, Date, Country Code, IP Address, and Device Metadata. Carrier is generated/assigned during the data-processing pipeline and is used as the target for network selection.

3. New / Engineered Columns
The preprocessing pipeline creates the following additional contextual features: Hour_of_Day, Day_of_Week, Is_Weekend, Geohash_Zone, Traffic_Load_Index, 5G_Capability, Roaming_Status, Horizontal_Accuracy, Signal_Reliability_Score, and Carrier. The code also derives IP Address and Device Metadata where required during dataset enrichment.

4. Feature Engineering & Signal Simulation
GPS coordinates are converted into Geohash_Zone values, timestamps are transformed into Hour_of_Day, Day_of_Week and Is_Weekend, and traffic conditions are represented using Traffic_Load_Index. The apply_signal_physics logic simulates signal strength using tower-distance calculations, density-based dampening and atmospheric noise, from which Horizontal_Accuracy and Signal_Reliability_Score are calculated.

5. ML Input Features
The final ML/RL feature set uses Latitude, Longitude, Hour_of_Day, Traffic_Load_Index, 5G_Capability, Roaming_Status, Horizontal_Accuracy, Signal_Reliability_Score and Geohash_Zone. Carrier is used as the target label for evaluating network-selection performance.

6. Data Preprocessing
The dataset is divided into 80% training and 20% testing data using stratified splitting. Geohash_Zone is handled using One-Hot Encoding, numerical features are normalized using StandardScaler, and Carrier labels are converted using Label Encoding. The encoders are fitted only on the training data to avoid data leakage.

7. Machine Learning Models
Four supervised ML algorithms are trained and compared: Logistic Regression, K-Nearest Neighbors (KNN), Random Forest, and Gradient Boosting. Gradient Boosting achieved the highest ML test accuracy of 81.23%, followed by KNN at 76.44%, Random Forest at 73.70%, and Logistic Regression at 61.24%.

8. Reinforcement Learning Models
A PyTorch-based DeepPolicyNet is used with ReLU hidden layers, a softmax output layer, and the Adam optimizer. Four RL approaches are evaluated: DQN, Double DQN, REINFORCE, and Advantage Actor-Critic (A2C), with training performed for 100 epochs.

9. Highest Accuracy & Best Model
A2C achieved the highest overall test accuracy of 83.52%. REINFORCE achieved 83.50%, Double DQN 83.49%, and DQN 83.39%. The A2C model was selected as the best RL policy and saved for deployment, while Gradient Boosting was the best-performing ML classifier at 81.23%.

10. Deployment & Real-Time Recommendation
The trained models are integrated with a Flask backend for online inference. The system accepts Device ID, current carrier, country, latitude, longitude, date, time, and device model, processes the contextual information, and provides a proactive carrier recommendation among Verizon, T-Mobile, AT&T, and Sprint along with Traffic Load, 5G Capability, Roaming Status, Horizontal Accuracy, Signal Reliability Score, and the reason for the recommendation. The project demo is available at: https://youtu.be/DWQ_oWB4xDI

Automated API Load Testing & Performance Analytics:-
Automated API Load Testing and Performance Analytics validates the production scalability and thread-safety of our hybrid reinforcement learning network selector. The system processed a total of 200,000 requests streamed from the dataset against the Flask backend. Out of these, 199,676 requests resulted in successful API responses, yielding an impressive success rate of 99.84%. The average API latency across all active multithreaded requests was recorded at 233.02 milliseconds, demonstrating high-speed execution under heavy concurrent load. A maximum peak latency of 5,771.81 milliseconds occurred due to initial thread-pool queue saturation and server cold-start backpressure. These comprehensive performance metrics provide audit-ready analytical proof of the system's enterprise-grade reliability and throughput

Enterprise Dataset Expansion & Advanced Feature Synthesis:-
To bridge the gap toward enterprise-grade readiness, an advanced data synthesis module (extended_dataset_tasks.py) was engineered to programmatically inject five critical real-world telemetry parameters across the entire dataset without modifying core training files. This extension tracks dynamic user mobility states (stationary, pedestrian, vehicular), assigns application slicing profiles (URLLC critical vs. eMBB high-bandwidth), calculates thermal battery drain rates, models core network jitter and packet loss, and computes a unified composite reinforcement learning reward score. To validate system execution instantly, a companion verification script (demo_extended.py) performs stratified random sampling to output dynamic analytical reports, ensuring robust performance under complex real-world edge cases.

 Podman Deployment Demonstration:-
This repository serves as the live deployment demonstration for the Context-Aware Proactive Network Selection framework, showcasing a containerized, full-stack application built to optimize mobile Quality of Service (QoS) using machine learning metrics. To ensure optimal performance for the interactive web dashboard while maintaining data integrity, this demo utilizes a sampled version of the extended network telemetry dataset. The application features a dual-mode Flask API engineered to handle both real-time data sampling for rapid frontend streaming in "Live Telemetry" mode, and deep database queries for specific device IDs in "DB Query Search" mode. Built using Python, Flask, HTML, CSS, and JavaScript, the system ensures enterprise-grade security by being containerized with Podman within a Windows Subsystem for Linux (WSL2) environment, leveraging a rootless, daemonless architecture and isolated Linux IP resolution. While this repository is dedicated solely to the deployment and UI demonstration, the core Reinforcement Learning algorithms (A2C, DQN), comprehensive machine learning models, and the complete un-sampled dataset are maintained in a separate repository. A full video demonstration of the system and its Podman deployment can be viewed on YouTube at https://youtu.be/AsjGI_re1xw.
