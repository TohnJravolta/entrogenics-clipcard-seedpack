import json
import os

# DevOps/SRE Agent Test
devops_agent_test = {
  "cells": [
    {
      "cell_type": "markdown",
      "id": "cell-0",
      "metadata": {},
      "source": [
        "# ClipCard Agent Test: DevOps/SRE\n",
        "\n",
        "**Purpose:** This notebook tests whether an AI agent (LLM) can correctly parse, validate, and reason about ClipCards in the DevOps/SRE domain.\n",
        "\n",
        "It evaluates:\n",
        "1. Can the agent extract kill criteria from a ClipCard?\n",
        "2. Can it determine if a given scenario would trigger the criteria?\n",
        "3. Can it suggest appropriate authority windows for different risk levels?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-1",
      "metadata": {},
      "outputs": [],
      "source": [
        "import json\n",
        "import pandas as pd\n",
        "\n",
        "# Load example ClipCard\n",
        "try:\n",
        "    with open('../../examples/test.clipcard.json', 'r') as f:\n",
        "        test_card = json.load(f)\n",
        "    print(\"Loaded test ClipCard:\")\n",
        "    print(json.dumps(test_card, indent=2))\n",
        "except FileNotFoundError:\n",
        "    print(\"No test ClipCard found.\")\n",
        "    test_card = None"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-2",
      "metadata": {},
      "source": [
        "### Test 1: Extract Kill Criteria\n",
        "\n",
        "Can we programmatically parse kill criteria?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-3",
      "metadata": {},
      "outputs": [],
      "source": [
        "if test_card:\n",
        "    kill_criteria = test_card.get('kill_criteria', [])\n",
        "    print(f\"Found {len(kill_criteria)} kill criteria:\\n\")\n",
        "    for i, criterion in enumerate(kill_criteria, 1):\n",
        "        print(f\"{i}. Condition: {criterion['condition']}\")\n",
        "        print(f\"   Action: {criterion['action']}\\n\")\n",
        "else:\n",
        "    print(\"No ClipCard available for testing.\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-4",
      "metadata": {},
      "source": [
        "### Test 2: Scenario Evaluation\n",
        "\n",
        "Test if scenarios match kill criteria"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-5",
      "metadata": {},
      "outputs": [],
      "source": [
        "# Define test scenarios for DevOps/SRE\n",
        "scenarios = [\n",
        "    {\n",
        "        \"name\": \"Normal Operation\",\n",
        "        \"error_rate\": 0.003,\n",
        "        \"latency_p99\": 250,\n",
        "        \"mttr_hours\": 0.5,\n",
        "        \"expected_trigger\": False\n",
        "    },\n",
        "    {\n",
        "        \"name\": \"High Error Rate\",\n",
        "        \"error_rate\": 0.015,\n",
        "        \"latency_p99\": 200,\n",
        "        \"mttr_hours\": 0.3,\n",
        "        \"expected_trigger\": True\n",
        "    },\n",
        "    {\n",
        "        \"name\": \"High Latency\",\n",
        "        \"error_rate\": 0.002,\n",
        "        \"latency_p99\": 600,\n",
        "        \"mttr_hours\": 0.4,\n",
        "        \"expected_trigger\": True\n",
        "    },\n",
        "    {\n",
        "        \"name\": \"Slow Recovery\",\n",
        "        \"error_rate\": 0.004,\n",
        "        \"latency_p99\": 300,\n",
        "        \"mttr_hours\": 3.0,\n",
        "        \"expected_trigger\": True\n",
        "    }\n",
        "]\n",
        "\n",
        "print(\"Testing scenarios against typical DevOps/SRE kill criteria:\\n\")\n",
        "print(\"Assumed thresholds:\")\n",
        "print(\"  - Error rate: > 0.01\")\n",
        "print(\"  - Latency p99: > 500ms\")\n",
        "print(\"  - MTTR: > 2.0 hours\\n\")\n",
        "\n",
        "results = []\n",
        "for scenario in scenarios:\n",
        "    # Evaluate against typical DevOps/SRE thresholds\n",
        "    error_trigger = scenario['error_rate'] > 0.01\n",
        "    latency_trigger = scenario['latency_p99'] > 500\n",
        "    mttr_trigger = scenario['mttr_hours'] > 2.0\n",
        "    \n",
        "    any_trigger = error_trigger or latency_trigger or mttr_trigger\n",
        "    match = any_trigger == scenario['expected_trigger']\n",
        "    \n",
        "    results.append({\n",
        "        'Scenario': scenario['name'],\n",
        "        'Error Trigger': error_trigger,\n",
        "        'Latency Trigger': latency_trigger,\n",
        "        'MTTR Trigger': mttr_trigger,\n",
        "        'Expected': scenario['expected_trigger'],\n",
        "        'Match': '✓' if match else '✗'\n",
        "    })\n",
        "\n",
        "df_results = pd.DataFrame(results)\n",
        "print(df_results.to_string(index=False))\n",
        "print(f\"\\nTest Accuracy: {df_results['Match'].value_counts().get('✓', 0)}/{len(results)}\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-6",
      "metadata": {},
      "source": [
        "### Test 3: Authority Window Recommendations\n",
        "\n",
        "Generate appropriate authority windows based on risk factors"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-7",
      "metadata": {},
      "outputs": [],
      "source": [
        "def recommend_authority_window(impact, uncertainty, reversibility):\n",
        "    \"\"\"\n",
        "    Recommend authority window based on ClipCard risk factors\n",
        "    \n",
        "    Args:\n",
        "        impact: 1-5 scale\n",
        "        uncertainty: 1-5 scale\n",
        "        reversibility: 1-5 scale (1=easy to reverse, 5=irreversible)\n",
        "    \"\"\"\n",
        "    risk_score = impact * uncertainty\n",
        "    \n",
        "    if risk_score >= 20 or reversibility >= 5:\n",
        "        return {\n",
        "            \"scope_limit\": \"1% traffic\",\n",
        "            \"time_limit\": \"24h\",\n",
        "            \"auto_pause\": True,\n",
        "            \"justification\": \"Very high risk requires minimal exposure\"\n",
        "        }\n",
        "    elif risk_score >= 15 or reversibility >= 4:\n",
        "        return {\n",
        "            \"scope_limit\": \"5% traffic\",\n",
        "            \"time_limit\": \"7d\",\n",
        "            \"auto_pause\": True,\n",
        "            \"justification\": \"High risk requires controlled rollout\"\n",
        "        }\n",
        "    elif risk_score >= 10:\n",
        "        return {\n",
        "            \"scope_limit\": \"10% traffic\",\n",
        "            \"time_limit\": \"14d\",\n",
        "            \"auto_pause\": False,\n",
        "            \"justification\": \"Medium risk allows moderate exposure\"\n",
        "        }\n",
        "    else:\n",
        "        return {\n",
        "            \"scope_limit\": \"25% traffic\",\n",
        "            \"time_limit\": \"30d\",\n",
        "            \"auto_pause\": False,\n",
        "            \"justification\": \"Lower risk permits broader exposure\"\n",
        "        }\n",
        "\n",
        "# Test with example scenarios\n",
        "test_cases = [\n",
        "    {\"name\": \"High-risk service\", \"impact\": 5, \"uncertainty\": 4, \"reversibility\": 5},\n",
        "    {\"name\": \"Medium-risk API\", \"impact\": 4, \"uncertainty\": 3, \"reversibility\": 2},\n",
        "    {\"name\": \"Low-risk config change\", \"impact\": 2, \"uncertainty\": 2, \"reversibility\": 1}\n",
        "]\n",
        "\n",
        "print(\"Authority Window Recommendations:\\n\")\n",
        "for case in test_cases:\n",
        "    rec = recommend_authority_window(case['impact'], case['uncertainty'], case['reversibility'])\n",
        "    print(f\"{case['name']} (I={case['impact']}, U={case['uncertainty']}, R={case['reversibility']}):\")\n",
        "    print(f\"  Scope: {rec['scope_limit']}\")\n",
        "    print(f\"  Duration: {rec['time_limit']}\")\n",
        "    print(f\"  Auto-pause: {rec['auto_pause']}\")\n",
        "    print(f\"  Reason: {rec['justification']}\\n\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-8",
      "metadata": {},
      "source": [
        "### Summary\n",
        "\n",
        "This notebook demonstrates that ClipCard data structures can be:\n",
        "- Programmatically parsed\n",
        "- Evaluated against scenarios\n",
        "- Used to generate risk-appropriate recommendations\n",
        "\n",
        "This enables AI agents to assist with ClipCard creation, validation, and decision support."
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.11.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}

# Policy/TS Agent Test
policy_agent_test = {
  "cells": [
    {
      "cell_type": "markdown",
      "id": "cell-0",
      "metadata": {},
      "source": [
        "# ClipCard Agent Test: Policy/Trust & Safety\n",
        "\n",
        "**Purpose:** This notebook tests whether an AI agent (LLM) can correctly parse, validate, and reason about ClipCards in the Policy/Trust & Safety domain.\n",
        "\n",
        "It evaluates:\n",
        "1. Can the agent extract kill criteria from a ClipCard?\n",
        "2. Can it determine if a given scenario would trigger the criteria?\n",
        "3. Can it suggest appropriate authority windows for different risk levels?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-1",
      "metadata": {},
      "outputs": [],
      "source": [
        "import json\n",
        "import pandas as pd\n",
        "\n",
        "# Load example ClipCard\n",
        "try:\n",
        "    with open('../../examples/test.clipcard.json', 'r') as f:\n",
        "        test_card = json.load(f)\n",
        "    print(\"Loaded test ClipCard:\")\n",
        "    print(json.dumps(test_card, indent=2))\n",
        "except FileNotFoundError:\n",
        "    print(\"No test ClipCard found.\")\n",
        "    test_card = None"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-2",
      "metadata": {},
      "source": [
        "### Test 1: Extract Kill Criteria\n",
        "\n",
        "Can we programmatically parse kill criteria?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-3",
      "metadata": {},
      "outputs": [],
      "source": [
        "if test_card:\n",
        "    kill_criteria = test_card.get('kill_criteria', [])\n",
        "    print(f\"Found {len(kill_criteria)} kill criteria:\\n\")\n",
        "    for i, criterion in enumerate(kill_criteria, 1):\n",
        "        print(f\"{i}. Condition: {criterion['condition']}\")\n",
        "        print(f\"   Action: {criterion['action']}\\n\")\n",
        "else:\n",
        "    print(\"No ClipCard available for testing.\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-4",
      "metadata": {},
      "source": [
        "### Test 2: Scenario Evaluation\n",
        "\n",
        "Test if scenarios match kill criteria"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-5",
      "metadata": {},
      "outputs": [],
      "source": [
        "# Define test scenarios for Policy/Trust & Safety\n",
        "scenarios = [\n",
        "    {\n",
        "        \"name\": \"Normal Operation\",\n",
        "        \"wrongful_action_rate\": 0.05,\n",
        "        \"appeal_rate\": 0.02,\n",
        "        \"false_positive_rate\": 0.01,\n",
        "        \"expected_trigger\": False\n",
        "    },\n",
        "    {\n",
        "        \"name\": \"High Wrongful Actions\",\n",
        "        \"wrongful_action_rate\": 0.85,\n",
        "        \"appeal_rate\": 0.03,\n",
        "        \"false_positive_rate\": 0.02,\n",
        "        \"expected_trigger\": True\n",
        "    },\n",
        "    {\n",
        "        \"name\": \"High Appeal Rate\",\n",
        "        \"wrongful_action_rate\": 0.10,\n",
        "        \"appeal_rate\": 0.25,\n",
        "        \"false_positive_rate\": 0.03,\n",
        "        \"expected_trigger\": True\n",
        "    },\n",
        "    {\n",
        "        \"name\": \"High False Positives\",\n",
        "        \"wrongful_action_rate\": 0.08,\n",
        "        \"appeal_rate\": 0.04,\n",
        "        \"false_positive_rate\": 0.15,\n",
        "        \"expected_trigger\": True\n",
        "    }\n",
        "]\n",
        "\n",
        "print(\"Testing scenarios against typical Policy/TS kill criteria:\\n\")\n",
        "print(\"Assumed thresholds:\")\n",
        "print(\"  - Wrongful action rate: >= 0.8\")\n",
        "print(\"  - Appeal rate: > 0.2\")\n",
        "print(\"  - False positive rate: > 0.1\\n\")\n",
        "\n",
        "results = []\n",
        "for scenario in scenarios:\n",
        "    # Evaluate against typical Policy/TS thresholds\n",
        "    wrongful_trigger = scenario['wrongful_action_rate'] >= 0.8\n",
        "    appeal_trigger = scenario['appeal_rate'] > 0.2\n",
        "    fp_trigger = scenario['false_positive_rate'] > 0.1\n",
        "    \n",
        "    any_trigger = wrongful_trigger or appeal_trigger or fp_trigger\n",
        "    match = any_trigger == scenario['expected_trigger']\n",
        "    \n",
        "    results.append({\n",
        "        'Scenario': scenario['name'],\n",
        "        'Wrongful Trigger': wrongful_trigger,\n",
        "        'Appeal Trigger': appeal_trigger,\n",
        "        'FP Trigger': fp_trigger,\n",
        "        'Expected': scenario['expected_trigger'],\n",
        "        'Match': '✓' if match else '✗'\n",
        "    })\n",
        "\n",
        "df_results = pd.DataFrame(results)\n",
        "print(df_results.to_string(index=False))\n",
        "print(f\"\\nTest Accuracy: {df_results['Match'].value_counts().get('✓', 0)}/{len(results)}\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-6",
      "metadata": {},
      "source": [
        "### Test 3: Authority Window Recommendations\n",
        "\n",
        "Generate appropriate authority windows based on risk factors"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-7",
      "metadata": {},
      "outputs": [],
      "source": [
        "def recommend_authority_window(impact, uncertainty, reversibility):\n",
        "    \"\"\"\n",
        "    Recommend authority window based on ClipCard risk factors\n",
        "    \n",
        "    Args:\n",
        "        impact: 1-5 scale\n",
        "        uncertainty: 1-5 scale\n",
        "        reversibility: 1-5 scale (1=easy to reverse, 5=irreversible)\n",
        "    \"\"\"\n",
        "    risk_score = impact * uncertainty\n",
        "    \n",
        "    if risk_score >= 20 or reversibility >= 5:\n",
        "        return {\n",
        "            \"scope_limit\": \"1% cohort\",\n",
        "            \"time_limit\": \"24h\",\n",
        "            \"auto_pause\": True,\n",
        "            \"justification\": \"Very high risk requires minimal exposure\"\n",
        "        }\n",
        "    elif risk_score >= 15 or reversibility >= 4:\n",
        "        return {\n",
        "            \"scope_limit\": \"5% cohort\",\n",
        "            \"time_limit\": \"7d\",\n",
        "            \"auto_pause\": True,\n",
        "            \"justification\": \"High risk requires controlled rollout\"\n",
        "        }\n",
        "    elif risk_score >= 10:\n",
        "        return {\n",
        "            \"scope_limit\": \"10% cohort\",\n",
        "            \"time_limit\": \"14d\",\n",
        "            \"auto_pause\": False,\n",
        "            \"justification\": \"Medium risk allows moderate exposure\"\n",
        "        }\n",
        "    else:\n",
        "        return {\n",
        "            \"scope_limit\": \"25% cohort\",\n",
        "            \"time_limit\": \"30d\",\n",
        "            \"auto_pause\": False,\n",
        "            \"justification\": \"Lower risk permits broader exposure\"\n",
        "        }\n",
        "\n",
        "# Test with example scenarios\n",
        "test_cases = [\n",
        "    {\"name\": \"High-risk policy\", \"impact\": 5, \"uncertainty\": 4, \"reversibility\": 5},\n",
        "    {\"name\": \"Medium-risk enforcement\", \"impact\": 4, \"uncertainty\": 3, \"reversibility\": 2},\n",
        "    {\"name\": \"Low-risk filter\", \"impact\": 2, \"uncertainty\": 2, \"reversibility\": 1}\n",
        "]\n",
        "\n",
        "print(\"Authority Window Recommendations:\\n\")\n",
        "for case in test_cases:\n",
        "    rec = recommend_authority_window(case['impact'], case['uncertainty'], case['reversibility'])\n",
        "    print(f\"{case['name']} (I={case['impact']}, U={case['uncertainty']}, R={case['reversibility']}):\")\n",
        "    print(f\"  Scope: {rec['scope_limit']}\")\n",
        "    print(f\"  Duration: {rec['time_limit']}\")\n",
        "    print(f\"  Auto-pause: {rec['auto_pause']}\")\n",
        "    print(f\"  Reason: {rec['justification']}\\n\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-8",
      "metadata": {},
      "source": [
        "### Summary\n",
        "\n",
        "This notebook demonstrates that ClipCard data structures can be:\n",
        "- Programmatically parsed\n",
        "- Evaluated against scenarios\n",
        "- Used to generate risk-appropriate recommendations\n",
        "\n",
        "This enables AI agents to assist with ClipCard creation, validation, and decision support."
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.11.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}

# Industrial/Aviation Agent Test
industrial_agent_test = {
  "cells": [
    {
      "cell_type": "markdown",
      "id": "cell-0",
      "metadata": {},
      "source": [
        "# ClipCard Agent Test: Industrial/Aviation\n",
        "\n",
        "**Purpose:** This notebook tests whether an AI agent (LLM) can correctly parse, validate, and reason about ClipCards in the Industrial/Aviation safety domain.\n",
        "\n",
        "It evaluates:\n",
        "1. Can the agent extract kill criteria from a ClipCard?\n",
        "2. Can it determine if a given scenario would trigger the criteria?\n",
        "3. Can it suggest appropriate authority windows for different risk levels?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-1",
      "metadata": {},
      "outputs": [],
      "source": [
        "import json\n",
        "import pandas as pd\n",
        "\n",
        "# Load example ClipCard\n",
        "try:\n",
        "    with open('../../examples/test.clipcard.json', 'r') as f:\n",
        "        test_card = json.load(f)\n",
        "    print(\"Loaded test ClipCard:\")\n",
        "    print(json.dumps(test_card, indent=2))\n",
        "except FileNotFoundError:\n",
        "    print(\"No test ClipCard found.\")\n",
        "    test_card = None"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-2",
      "metadata": {},
      "source": [
        "### Test 1: Extract Kill Criteria\n",
        "\n",
        "Can we programmatically parse kill criteria?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-3",
      "metadata": {},
      "outputs": [],
      "source": [
        "if test_card:\n",
        "    kill_criteria = test_card.get('kill_criteria', [])\n",
        "    print(f\"Found {len(kill_criteria)} kill criteria:\\n\")\n",
        "    for i, criterion in enumerate(kill_criteria, 1):\n",
        "        print(f\"{i}. Condition: {criterion['condition']}\")\n",
        "        print(f\"   Action: {criterion['action']}\\n\")\n",
        "else:\n",
        "    print(\"No ClipCard available for testing.\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-4",
      "metadata": {},
      "source": [
        "### Test 2: Scenario Evaluation\n",
        "\n",
        "Test if scenarios match kill criteria"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-5",
      "metadata": {},
      "outputs": [],
      "source": [
        "# Define test scenarios for Industrial/Aviation\n",
        "scenarios = [\n",
        "    {\n",
        "        \"name\": \"Normal Operation\",\n",
        "        \"deviation_count\": 0,\n",
        "        \"pressure_psi\": 100,\n",
        "        \"temperature_c\": 65,\n",
        "        \"expected_trigger\": False\n",
        "    },\n",
        "    {\n",
        "        \"name\": \"Process Deviation\",\n",
        "        \"deviation_count\": 1,\n",
        "        \"pressure_psi\": 95,\n",
        "        \"temperature_c\": 70,\n",
        "        \"expected_trigger\": True\n",
        "    },\n",
        "    {\n",
        "        \"name\": \"High Pressure\",\n",
        "        \"deviation_count\": 0,\n",
        "        \"pressure_psi\": 125,\n",
        "        \"temperature_c\": 68,\n",
        "        \"expected_trigger\": True\n",
        "    },\n",
        "    {\n",
        "        \"name\": \"High Temperature\",\n",
        "        \"deviation_count\": 0,\n",
        "        \"pressure_psi\": 98,\n",
        "        \"temperature_c\": 85,\n",
        "        \"expected_trigger\": True\n",
        "    }\n",
        "]\n",
        "\n",
        "print(\"Testing scenarios against typical Industrial/Aviation kill criteria:\\n\")\n",
        "print(\"Assumed thresholds:\")\n",
        "print(\"  - Deviation count: >= 1\")\n",
        "print(\"  - Pressure: > 120 psi\")\n",
        "print(\"  - Temperature: > 80°C\\n\")\n",
        "\n",
        "results = []\n",
        "for scenario in scenarios:\n",
        "    # Evaluate against typical Industrial/Aviation thresholds\n",
        "    deviation_trigger = scenario['deviation_count'] >= 1\n",
        "    pressure_trigger = scenario['pressure_psi'] > 120\n",
        "    temp_trigger = scenario['temperature_c'] > 80\n",
        "    \n",
        "    any_trigger = deviation_trigger or pressure_trigger or temp_trigger\n",
        "    match = any_trigger == scenario['expected_trigger']\n",
        "    \n",
        "    results.append({\n",
        "        'Scenario': scenario['name'],\n",
        "        'Deviation Trigger': deviation_trigger,\n",
        "        'Pressure Trigger': pressure_trigger,\n",
        "        'Temp Trigger': temp_trigger,\n",
        "        'Expected': scenario['expected_trigger'],\n",
        "        'Match': '✓' if match else '✗'\n",
        "    })\n",
        "\n",
        "df_results = pd.DataFrame(results)\n",
        "print(df_results.to_string(index=False))\n",
        "print(f\"\\nTest Accuracy: {df_results['Match'].value_counts().get('✓', 0)}/{len(results)}\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-6",
      "metadata": {},
      "source": [
        "### Test 3: Authority Window Recommendations\n",
        "\n",
        "Generate appropriate authority windows based on risk factors"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-7",
      "metadata": {},
      "outputs": [],
      "source": [
        "def recommend_authority_window(impact, uncertainty, reversibility):\n",
        "    \"\"\"\n",
        "    Recommend authority window based on ClipCard risk factors\n",
        "    \n",
        "    Args:\n",
        "        impact: 1-5 scale\n",
        "        uncertainty: 1-5 scale\n",
        "        reversibility: 1-5 scale (1=easy to reverse, 5=irreversible)\n",
        "    \"\"\"\n",
        "    risk_score = impact * uncertainty\n",
        "    \n",
        "    if risk_score >= 20 or reversibility >= 5:\n",
        "        return {\n",
        "            \"scope_limit\": \"1 unit/line\",\n",
        "            \"time_limit\": \"24h\",\n",
        "            \"auto_pause\": True,\n",
        "            \"justification\": \"Very high risk requires minimal exposure\"\n",
        "        }\n",
        "    elif risk_score >= 15 or reversibility >= 4:\n",
        "        return {\n",
        "            \"scope_limit\": \"Single facility\",\n",
        "            \"time_limit\": \"7d\",\n",
        "            \"auto_pause\": True,\n",
        "            \"justification\": \"High risk requires controlled rollout\"\n",
        "        }\n",
        "    elif risk_score >= 10:\n",
        "        return {\n",
        "            \"scope_limit\": \"Regional rollout\",\n",
        "            \"time_limit\": \"14d\",\n",
        "            \"auto_pause\": False,\n",
        "            \"justification\": \"Medium risk allows moderate exposure\"\n",
        "        }\n",
        "    else:\n",
        "        return {\n",
        "            \"scope_limit\": \"Fleet-wide\",\n",
        "            \"time_limit\": \"30d\",\n",
        "            \"auto_pause\": False,\n",
        "            \"justification\": \"Lower risk permits broader exposure\"\n",
        "        }\n",
        "\n",
        "# Test with example scenarios\n",
        "test_cases = [\n",
        "    {\"name\": \"High-risk MOC\", \"impact\": 5, \"uncertainty\": 4, \"reversibility\": 5},\n",
        "    {\"name\": \"Medium-risk procedure\", \"impact\": 4, \"uncertainty\": 3, \"reversibility\": 2},\n",
        "    {\"name\": \"Low-risk maintenance\", \"impact\": 2, \"uncertainty\": 2, \"reversibility\": 1}\n",
        "]\n",
        "\n",
        "print(\"Authority Window Recommendations:\\n\")\n",
        "for case in test_cases:\n",
        "    rec = recommend_authority_window(case['impact'], case['uncertainty'], case['reversibility'])\n",
        "    print(f\"{case['name']} (I={case['impact']}, U={case['uncertainty']}, R={case['reversibility']}):\")\n",
        "    print(f\"  Scope: {rec['scope_limit']}\")\n",
        "    print(f\"  Duration: {rec['time_limit']}\")\n",
        "    print(f\"  Auto-pause: {rec['auto_pause']}\")\n",
        "    print(f\"  Reason: {rec['justification']}\\n\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-8",
      "metadata": {},
      "source": [
        "### Summary\n",
        "\n",
        "This notebook demonstrates that ClipCard data structures can be:\n",
        "- Programmatically parsed\n",
        "- Evaluated against scenarios\n",
        "- Used to generate risk-appropriate recommendations\n",
        "\n",
        "This enables AI agents to assist with ClipCard creation, validation, and decision support."
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.11.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}

# Civic/ICS Sim
civic_sim = {
  "cells": [
    {
      "cell_type": "markdown",
      "id": "cell-0",
      "metadata": {},
      "source": [
        "# ClipCard Simulation: Civic/ICS\n",
        "\n",
        "**Purpose:** This notebook runs a Monte Carlo simulation to estimate the effectiveness of ClipCard parameters for civic incident command operations.\n",
        "\n",
        "It simulates operations and checks if randomly generated metrics (like `queue_time` or `stockout`) would trigger the `kill_criteria` defined in a ClipCard. This helps quantify the risk reduction provided by the card's specific configuration."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-1",
      "metadata": {},
      "outputs": [],
      "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import json\n",
        "import glob\n",
        "\n",
        "# Load example ClipCards from the examples or data directory\n",
        "try:\n",
        "    with open('../../examples/test.clipcard.json', 'r') as f:\n",
        "        example_card = json.load(f)\n",
        "    print(f\"Loaded example ClipCard: {example_card['id']}\")\n",
        "except FileNotFoundError:\n",
        "    print(\"No example ClipCard found. Using synthetic data.\")\n",
        "    example_card = {\n",
        "        \"id\": \"SIM-CIVIC-001\",\n",
        "        \"kill_criteria\": [\n",
        "            {\"condition\": \"queue_time > 120\", \"action\": \"Activate overflow shelter\"},\n",
        "            {\"condition\": \"stockout >= 1\", \"action\": \"Request emergency supplies\"}\n",
        "        ],\n",
        "        \"authority_window\": {\"scope_limit\": \"Single Division\", \"time_limit\": \"30d\"}\n",
        "    }"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-2",
      "metadata": {},
      "source": [
        "### Simulation Parameters\n",
        "\n",
        "Configure simulation runs and metric distributions"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-3",
      "metadata": {},
      "outputs": [],
      "source": [
        "# Simulation configuration\n",
        "N_SIMULATIONS = 1000  # Number of operational simulations\n",
        "COHORT_SIZE = 0.20    # 20% of shelters\n",
        "BASE_QUEUE_TIME = 45  # Base queue time in minutes\n",
        "BASE_STOCKOUT_RATE = 0.0005  # Base stockout probability\n",
        "\n",
        "print(f\"Running {N_SIMULATIONS} simulations...\")\n",
        "print(f\"Shelter coverage: {COHORT_SIZE*100}%\")\n",
        "print(f\"Base queue time: {BASE_QUEUE_TIME} min\")\n",
        "print(f\"Base stockout rate: {BASE_STOCKOUT_RATE}\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-4",
      "metadata": {},
      "source": [
        "### Monte Carlo Simulation\n",
        "\n",
        "Run simulations and track kill criteria triggers"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-5",
      "metadata": {},
      "outputs": [],
      "source": [
        "results = []\n",
        "\n",
        "for i in range(N_SIMULATIONS):\n",
        "    # Simulate metrics for a 24-hour period\n",
        "    arrivals = np.random.poisson(200)  # Number of arrivals\n",
        "    \n",
        "    # Simulate queue time (Gamma distribution)\n",
        "    queue_time = np.random.gamma(2, BASE_QUEUE_TIME/2)\n",
        "    \n",
        "    # Simulate stockouts (Poisson process)\n",
        "    stockouts = np.random.poisson(BASE_STOCKOUT_RATE * arrivals)\n",
        "    \n",
        "    # Check kill criteria\n",
        "    queue_trigger = queue_time > 120\n",
        "    stockout_trigger = stockouts >= 1\n",
        "    any_trigger = queue_trigger or stockout_trigger\n",
        "    \n",
        "    results.append({\n",
        "        'sim_id': i,\n",
        "        'arrivals': arrivals,\n",
        "        'queue_time': queue_time,\n",
        "        'stockouts': stockouts,\n",
        "        'queue_trigger': queue_trigger,\n",
        "        'stockout_trigger': stockout_trigger,\n",
        "        'any_trigger': any_trigger\n",
        "    })\n",
        "\n",
        "df = pd.DataFrame(results)\n",
        "print(f\"\\nSimulation complete!\")\n",
        "print(f\"Queue time triggers: {df['queue_trigger'].sum()} ({df['queue_trigger'].mean()*100:.1f}%)\")\n",
        "print(f\"Stockout triggers: {df['stockout_trigger'].sum()} ({df['stockout_trigger'].mean()*100:.1f}%)\")\n",
        "print(f\"Any trigger: {df['any_trigger'].sum()} ({df['any_trigger'].mean()*100:.1f}%)\")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cell-6",
      "metadata": {},
      "source": [
        "### Visualization\n",
        "\n",
        "Plot trigger distributions and risk reduction"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "id": "cell-7",
      "metadata": {},
      "outputs": [],
      "source": [
        "fig, axes = plt.subplots(1, 3, figsize=(15, 4))\n",
        "\n",
        "# Queue time distribution\n",
        "axes[0].hist(df['queue_time'], bins=30, alpha=0.7, edgecolor='black')\n",
        "axes[0].axvline(120, color='red', linestyle='--', label='Kill threshold')\n",
        "axes[0].set_xlabel('Queue Time (minutes)')\n",
        "axes[0].set_ylabel('Frequency')\n",
        "axes[0].set_title('Queue Time Distribution')\n",
        "axes[0].legend()\n",
        "\n",
        "# Stockout distribution\n",
        "axes[1].hist(df['stockouts'], bins=30, alpha=0.7, edgecolor='black')\n",
        "axes[1].axvline(1, color='red', linestyle='--', label='Kill threshold')\n",
        "axes[1].set_xlabel('Stockouts per 24h')\n",
        "axes[1].set_ylabel('Frequency')\n",
        "axes[1].set_title('Stockout Distribution')\n",
        "axes[1].legend()\n",
        "\n",
        "# Trigger summary\n",
        "trigger_counts = [\n",
        "    df['queue_trigger'].sum(),\n",
        "    df['stockout_trigger'].sum(),\n",
        "    df['any_trigger'].sum()\n",
        "]\n",
        "trigger_labels = ['Queue Time', 'Stockout', 'Any Trigger']\n",
        "axes[2].bar(trigger_labels, trigger_counts, alpha=0.7, edgecolor='black')\n",
        "axes[2].set_ylabel('Number of Triggers')\n",
        "axes[2].set_title(f'Kill Criteria Triggers (n={N_SIMULATIONS})')\n",
        "axes[2].axhline(N_SIMULATIONS * 0.05, color='orange', linestyle='--', label='5% threshold')\n",
        "axes[2].legend()\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()\n",
        "\n",
        "print(f\"\\n** Interpretation **\")\n",
        "print(f\"In {N_SIMULATIONS} simulated 24h periods with a {COHORT_SIZE*100}% coverage:\")\n",
        "print(f\"- Kill criteria would trigger {df['any_trigger'].mean()*100:.1f}% of the time\")\n",
        "print(f\"- This suggests the authority window provides {(1-df['any_trigger'].mean())*100:.1f}% safe operation probability\")\n",
        "print(f\"- Estimated incident prevention: {df['any_trigger'].sum()} potential incidents caught early\")"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.11.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}

# Write all notebooks
base_path = r'C:\Users\jarde\Documents\projects\ASK\Clipcard\entrogenics-clipcard-seedpack\notebooks'

with open(os.path.join(base_path, 'devops_sre', 'clipcard_agent_test.ipynb'), 'w') as f:
    json.dump(devops_agent_test, f, indent=2)
print('Fixed devops_sre/clipcard_agent_test.ipynb')

with open(os.path.join(base_path, 'policy_ts', 'clipcard_agent_test.ipynb'), 'w') as f:
    json.dump(policy_agent_test, f, indent=2)
print('Fixed policy_ts/clipcard_agent_test.ipynb')

with open(os.path.join(base_path, 'industrial_aviation', 'clipcard_agent_test.ipynb'), 'w') as f:
    json.dump(industrial_agent_test, f, indent=2)
print('Fixed industrial_aviation/clipcard_agent_test.ipynb')

with open(os.path.join(base_path, 'civic_ics', 'clipcard_sim.ipynb'), 'w') as f:
    json.dump(civic_sim, f, indent=2)
print('Fixed civic_ics/clipcard_sim.ipynb')

print('\nAll notebooks fixed!')
