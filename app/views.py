import requests
from django.shortcuts import render,redirect
import openai
import threading

common_prefix ='Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string \"". \n \n Example 1: \n  Input: strs = ["flower","flow","flight"]\nOutput: "fl"\n \n Example 2:\n  Input: strs = ["dog","racecar","car"]\n Output: ""\nExplanation: There is no common prefix among the input strings.'
two_sum = 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n You may assume that each input would have exactly one solution, and you may not use the same element twice. \n \n Example 1: \n Input: nums = [2,7,11,15], target = 9 \n Output: [0,1] \n Explanation: Because nums[0] + nums[1] == 9, output = [0, 1]. \n \n Example 3: \n Input: nums = [3,3], target = 6 \n Output: [0,1]'
hint_used = 0 
problem =None
test_cases =  ""
flag_code = 0
openai.api_key = "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"
openai.api_key = openai.api_key

content = None
content_lock = threading.Lock()

def landing_page(request):

    global problem
    global test_cases
    if request.method == 'POST':
        if 'problem1' in request.POST:
            problem = common_prefix
            test_cases = 'Input: strs = ["","",""] Output: "", Input: strs = ["flower"] Output: "flower", Input: strs = ["1234", "12", "123"]  Output: ""'
            return redirect('execute_python_code')
        if 'problem2' in request.POST:
            problem = two_sum
            test_cases = "Input: nums = [2,7,11,15], target = 9  Output: [0,1],  Input: nums = [3,3], target = 6  Output: [0,1], Input: nums = [-2, 4, -6, 10], target = 2  Output: [0,1] "
            return redirect('execute_python_code')

    return render(request, 'landingpage.html', {})

def execute_java_code(request):
    global code
    global hint_used
    if request.method == 'POST':
        if 'run' in request.POST:
            code = request.POST.get('code')
            url = "https://api.jdoodle.com/v1/execute"

            client_id = "e65c1949d6893a3c99d282ec59917baf"  # Replace with your Jdoodle client ID
            client_secret = "20ec128dc49b443f22e19a0663558b1608ac40e87808cf59ae46977943d31137"  # Replace with your Jdoodle client secret

            payload = {
                "clientId": client_id,
                "clientSecret": client_secret,
                "script": code,
                "language": "java",
                "versionIndex": 3
            }

            response = requests.post(url, json=payload)
            result = response.json()
            output = result.get('output')
            #print(code)
            #evaluation_results = evaluate_code(code, test_cases)

            #print(evaluation_results)
            return render(request, 'home_java.html', {'output': output, 'code': code,'problem':problem})
        if 'hint'in request.POST:
            hint_used = 1
            code = request.POST.get('code') 
            prompt = "#provide a summarized high level approach brute force approach to solve the following problem in text in 5-6 points. Do not provide code" + '\n' + problem
            completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", 
                            max_tokens = 512,
                            temperature = 0.1,
                            messages=[{"role": "user", "content": prompt}]
                        )
            hint = completion["choices"][0]["message"]["content"]
            return render(request, 'home_java.html', {'hint': hint, 'code': code,'problem':problem})
        '''        
        if 'hint2' in request.POST:
            code = request.POST.get('code') 
            if len(code) < 10:
                prompt = "#Please provide a high level approach to solve the following problem. Do not give actual code just give high-level abstract approach to solve the problem." + '\n' + problem
            else:
                prompt = "#Please Give hints on what could be changed in the code to get the correct answer in a brute force approach. Do not provide actual code" + '\n' + problem +'\n' + code
            completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", 
                            max_tokens = 512,
                            temperature = 0.1,
                            messages=[{"role": "user", "content": prompt}]
                        )
            hint2 = completion["choices"][0]["message"]["content"]
    
            return render(request, 'home_java.html', {'hint2': hint2, 'code': code,'problem':problem})
        
        if 'hint3' in request.POST:
            code = request.POST.get('code') 
            if len(code) < 10:
                prompt = "#Please provide a high level approach to solve the following problem. Do not give actual code just give high-level abstract approach to solve the problem." + '\n' + problem
            else:
                prompt = "#Please Give hints on what could be changed in the code to get the correct answer in a most optimized approach. Do not provide actual code" + '\n' + problem +'\n' + code
            completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", 
                            max_tokens = 512,
                            temperature = 0.1,
                            messages=[{"role": "user", "content": prompt}]
                        )
            hint3 = completion["choices"][0]["message"]["content"]
            print(hint3)
            return render(request, 'home_java.html', {'hint3': hint3, 'code': code,'problem':problem})
        '''
        if 'feedback' in request.POST:
            global content
            code = request.POST.get('code')
            prompt = "#Is the following code correct for the problem? Check the code for all corner cases. Provide a detailed feedback on the time complexity, space complexity, and execution time. Also, suggest improvements for the code." +'\n' + problem + '\n' + code
            thread = threading.Thread(target=fetch_chatgpt_response, args=(prompt,))
            thread.start()

            return render(request, 'thank_you.html',{})

    return render(request, 'home_java.html',{'problem':problem})

    
def execute_python_code(request):
    global code
    global hint_used
    if request.method == 'POST':
        if 'run' in request.POST:
            code = request.POST.get('code')
            url = "https://api.jdoodle.com/v1/execute"

            client_id = "e65c1949d6893a3c99d282ec59917baf"  # Replace with your Jdoodle client ID
            client_secret = "20ec128dc49b443f22e19a0663558b1608ac40e87808cf59ae46977943d31137"  # Replace with your Jdoodle client secret

            payload = {
                "clientId": client_id,
                "clientSecret": client_secret,
                "script": code,
                "language": "python3",
                "versionIndex": 3
            }

            response = requests.post(url, json=payload)
            result = response.json()
            output = result.get('output')
            #print(code)
            #evaluation_results = evaluate_code(code, test_cases)

            #print(evaluation_results)
            return render(request, 'home_python.html', {'output': output, 'code': code,'problem':problem})
        
        if 'hint'in request.POST:
            hint_used = 1
            code = request.POST.get('code') 
            prompt = "#provide a high level approach brute force approach to solve the following problem in text. Do not provide code." + '\n' + problem
            completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", 
                            max_tokens = 512,
                            temperature = 0.1,
                            messages=[{"role": "user", "content": prompt}]
                        )
            hint = completion["choices"][0]["message"]["content"]
            
    
            return render(request, 'home_python.html', {'hint': hint, 'code': code,'problem':problem})
        '''
        if 'hint2' in request.POST:
            code = request.POST.get('code') 
            # if len(code) < 10:
            #     prompt = "#Please provide a high level approach to solve the following problem. Do not give actual code just give high-level abstract approach to solve the problem." + '\n' + problem
            # else:
            prompt = "#Give hints on what could be changed in the code to get the correct answer in a brute force approach. Do not provide actual code" + '\n' + problem +'\n' + code
            completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", 
                            max_tokens = 512,
                            temperature = 0.1,
                            messages=[{"role": "user", "content": prompt}]
                        )
            hint2 = completion["choices"][0]["message"]["content"]
            
    
            return render(request, 'home_python.html', {'hint2': hint2, 'code': code,'problem':problem})
        
        if 'hint3' in request.POST:
            code = request.POST.get('code') 
            # if len(code) < 10:
            #     prompt = "#Please provide a high level approach to solve the following problem. Do not give actual code just give high-level abstract approach to solve the problem." + '\n' + problem
            # else:
            prompt = "#Give hints on what could be changed in the code to get the correct answer in a most optimized approach. Do not provide actual code" + '\n' + problem +'\n' + code
            completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", 
                            max_tokens = 512,
                            temperature = 0.1,
                            messages=[{"role": "user", "content": prompt}]
                        )
            hint3 = completion["choices"][0]["message"]["content"]
            
    
            return render(request, 'home_python.html', {'hint3': hint3, 'code': code,'problem':problem})
        '''       
        if 'feedback' in request.POST:
            global content
            global flag_code 
            code = request.POST.get('code')
            if len(code) == 0:         
                flag_code = 1
                prompt = "Report user that no code was provided. suggest optimized code for the given problem statement provided after 'prblem:' " + "problem:" + '\n' + problem 
            else:
                prompt = "#Is the following code correct for the problem? Comment why it is not correct. Check the code for provided in test_cases. Report if given code passes the provided test cases. Provide a detailed feedback on the time complexity, space complexity, and execution time. Also, suggest improvements for the submitted code." + "problem:" + '\n' + problem + '\n' + "code:" + '\n' + code + '\n' + "test_cases:" + '\n' + test_cases
            thread = threading.Thread(target=fetch_chatgpt_response, args=(prompt,))
            thread.start()

            return render(request, 'thank_you.html',{})

    return render(request, 'home_python.html',{'problem':problem})



def fetch_chatgpt_response(prompt):
    global content
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        max_tokens = 3500,
        temperature = 0.1,
        messages=[{"role": "user", "content": prompt}]
        )
    content = completion["choices"][0]["message"]["content"]
    with content_lock:
        content = content

def feedback_result(request):
    global code,content
    #prompt = "# Is the following code correct for the problem? Check the code for all corner cases. Provide a detailed feedback on the time complexity, space complexity, and execution time. Also, suggest improvements for the code." + common_prefix + '\n' + code

    

    # Render the feedback.html template with the content value
    with content_lock:
        feedback_content = content
    # Retrieve the ChatGPT response from the completed API call
    #content = fetch_chatgpt_response(prompt)

    # Render the feedback.html template with the response content
    return render(request, 'feedback.html', {'content': feedback_content,'hint_used':hint_used,'flag_code':flag_code})



'''
def feedback_display(request):
    global code
    prompt = "# Is following a correct code for following problem? Check the code for all corner cases. Give me a detailed feedback based on the time complexity, space compexity and execution time. Also give me suggestions to further improve the code." + common_prefix + '\n' + code
    openai.api_key = openai.api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        max_tokens = 3000,
        temperature = 1.2,
        messages=[{"role": "user", "content": prompt}]
        )
    content = completion["choices"][0]["message"]["content"]
    
    return render(request, 'feedback.html',{'content':content})



def a_execute_python_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        url = "https://judge0-ce.p.rapidapi.com/submissions"

        headers = {
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
            "X-RapidAPI-Key": "18f0e441cemsh1e1c1f41e8f254fp1669bdjsn34093604cf87",  # Replace with your RapidAPI key
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "language_id": 71,  # Language ID for Python
            "source_code": code,
            "stdin": ""
        }

        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        print(result)  # Print the response for debugging

        # Get the result ID
        result_id = result.get('token')
        result_url = f"{url}/{result_id}"

        # Retry fetching the result if the token is not available
        while not result_id:
            time.sleep(1)
            response = requests.get(result_url, headers=headers)
            result = response.json()
            result_id = result.get('token')

        # Retrieve the result using the result ID
        

        # Retry fetching the result until it is completed
        while result.get('status').get('description') != "Accepted":
            time.sleep(1)
            response = requests.get(result_url, headers=headers)
            result = response.json()

        output = result['stdout']

        return render(request, 'home.html', {'output': output, 'code': code})

    return render(request, 'home.html')
'''
