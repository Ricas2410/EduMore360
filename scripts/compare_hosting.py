"""
Compare hosting performance: Render vs PythonAnywhere
Tests both sites with same load to compare performance
"""

import requests
import time
import threading
import json
from datetime import datetime

class HostingComparison:
    def __init__(self):
        self.sites = {
            'render': {
                'url': 'https://edumore360.onrender.com',
                'name': 'EduMore360 (Render - 512MB)',
                'memory': '512MB',
                'cost': '$0 (free) / $25 (pro)'
            },
            'pythonanywhere': {
                'url': 'https://ricasmart.pythonanywhere.com',
                'name': 'RicaSmart (PythonAnywhere - 1GB)',
                'memory': '1GB',
                'cost': '$0 (free) / $5 (hacker)'
            }
        }
        self.results = {}
    
    def test_single_request(self, site_key, endpoint="/"):
        """Test a single request to measure response time"""
        site = self.sites[site_key]
        url = site['url'] + endpoint
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=30)
            end_time = time.time()
            
            return {
                'success': response.status_code == 200,
                'response_time': (end_time - start_time) * 1000,
                'status_code': response.status_code,
                'content_length': len(response.content) if response.status_code == 200 else 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response_time': 30000  # Timeout
            }
    
    def test_concurrent_users(self, site_key, num_users=10, duration=30):
        """Test concurrent users on a site"""
        print(f"\n🧪 Testing {self.sites[site_key]['name']} with {num_users} users...")
        
        results = {
            'site': site_key,
            'users': num_users,
            'duration': duration,
            'requests': 0,
            'successful': 0,
            'failed': 0,
            'response_times': [],
            'errors': []
        }
        
        def user_simulation(user_id):
            """Simulate a single user"""
            session = requests.Session()
            start_time = time.time()
            
            while time.time() - start_time < duration:
                # Choose endpoint based on site
                if site_key == 'pythonanywhere':
                    endpoint = "/" if user_id % 2 == 0 else "/products/"
                else:
                    endpoint = "/"
                
                result = self.test_single_request(site_key, endpoint)
                
                results['requests'] += 1
                if result['success']:
                    results['successful'] += 1
                    results['response_times'].append(result['response_time'])
                else:
                    results['failed'] += 1
                    results['errors'].append(result.get('error', 'Unknown error'))
                
                # Wait between requests
                time.sleep(1)
        
        # Start user threads
        threads = []
        for i in range(num_users):
            thread = threading.Thread(target=user_simulation, args=(i,))
            thread.start()
            threads.append(thread)
            time.sleep(0.1)  # Stagger user start
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        return results
    
    def compare_sites(self, user_counts=[10, 25, 50]):
        """Compare both sites with different user counts"""
        print("🚀 Hosting Performance Comparison")
        print("=" * 80)
        print("Comparing Render (512MB) vs PythonAnywhere (1GB)")
        print("=" * 80)
        
        comparison_results = {}
        
        for user_count in user_counts:
            print(f"\n📊 Testing with {user_count} concurrent users...")
            print("-" * 50)
            
            comparison_results[user_count] = {}
            
            # Test both sites
            for site_key in ['render', 'pythonanywhere']:
                try:
                    result = self.test_concurrent_users(site_key, user_count, 30)
                    comparison_results[user_count][site_key] = result
                    
                    # Display immediate results
                    success_rate = (result['successful'] / max(result['requests'], 1)) * 100
                    avg_response = sum(result['response_times']) / max(len(result['response_times']), 1)
                    
                    print(f"   {self.sites[site_key]['name']}:")
                    print(f"      Requests: {result['requests']}")
                    print(f"      Success Rate: {success_rate:.1f}%")
                    print(f"      Avg Response: {avg_response:.0f}ms")
                    
                except Exception as e:
                    print(f"   ❌ {self.sites[site_key]['name']}: Error - {e}")
                    comparison_results[user_count][site_key] = {'error': str(e)}
        
        self.display_comparison(comparison_results)
        return comparison_results
    
    def display_comparison(self, results):
        """Display detailed comparison results"""
        print("\n" + "=" * 80)
        print("📊 DETAILED COMPARISON RESULTS")
        print("=" * 80)
        
        # Summary table
        print("\n📋 Performance Summary:")
        print(f"{'Users':<8} {'Platform':<25} {'Success Rate':<12} {'Avg Response':<15} {'Memory':<10}")
        print("-" * 80)
        
        for user_count in sorted(results.keys()):
            for site_key in ['render', 'pythonanywhere']:
                if site_key in results[user_count] and 'error' not in results[user_count][site_key]:
                    result = results[user_count][site_key]
                    success_rate = (result['successful'] / max(result['requests'], 1)) * 100
                    avg_response = sum(result['response_times']) / max(len(result['response_times']), 1)
                    
                    platform_name = self.sites[site_key]['name'][:24]
                    memory = self.sites[site_key]['memory']
                    
                    print(f"{user_count:<8} {platform_name:<25} {success_rate:>8.1f}% {avg_response:>10.0f}ms {memory:<10}")
                else:
                    platform_name = self.sites[site_key]['name'][:24]
                    print(f"{user_count:<8} {platform_name:<25} {'ERROR':<12} {'N/A':<15} {'N/A':<10}")
        
        # Winner analysis
        print("\n🏆 WINNER ANALYSIS:")
        
        for user_count in sorted(results.keys()):
            print(f"\n👥 {user_count} Users:")
            
            render_data = results[user_count].get('render', {})
            python_data = results[user_count].get('pythonanywhere', {})
            
            if 'error' not in render_data and 'error' not in python_data:
                render_success = (render_data['successful'] / max(render_data['requests'], 1)) * 100
                python_success = (python_data['successful'] / max(python_data['requests'], 1)) * 100
                
                render_response = sum(render_data['response_times']) / max(len(render_data['response_times']), 1)
                python_response = sum(python_data['response_times']) / max(len(python_data['response_times']), 1)
                
                # Determine winner
                if python_success > render_success + 5:  # 5% threshold
                    print(f"   🥇 Winner: PythonAnywhere (Better success rate: {python_success:.1f}% vs {render_success:.1f}%)")
                elif render_success > python_success + 5:
                    print(f"   🥇 Winner: Render (Better success rate: {render_success:.1f}% vs {python_success:.1f}%)")
                elif python_response < render_response * 0.8:  # 20% faster
                    print(f"   🥇 Winner: PythonAnywhere (Faster response: {python_response:.0f}ms vs {render_response:.0f}ms)")
                elif render_response < python_response * 0.8:
                    print(f"   🥇 Winner: Render (Faster response: {render_response:.0f}ms vs {python_response:.0f}ms)")
                else:
                    print(f"   🤝 Tie: Both platforms perform similarly")
            else:
                print(f"   ⚠️  Cannot compare due to errors")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        
        # Analyze overall performance
        render_wins = 0
        python_wins = 0
        
        for user_count in results.keys():
            render_data = results[user_count].get('render', {})
            python_data = results[user_count].get('pythonanywhere', {})
            
            if 'error' not in render_data and 'error' not in python_data:
                render_success = (render_data['successful'] / max(render_data['requests'], 1)) * 100
                python_success = (python_data['successful'] / max(python_data['requests'], 1)) * 100
                
                if python_success > render_success:
                    python_wins += 1
                elif render_success > python_success:
                    render_wins += 1
        
        if python_wins > render_wins:
            print("   🎯 PythonAnywhere performs better overall")
            print("   💰 Cost advantage: $5/month vs $25/month")
            print("   💾 Memory advantage: 1GB vs 512MB")
            print("   📈 Recommendation: Consider migrating to PythonAnywhere")
        elif render_wins > python_wins:
            print("   🎯 Render performs better overall")
            print("   ⚡ Better for high-performance needs")
            print("   📈 Recommendation: Stay on Render, consider upgrading plan")
        else:
            print("   🎯 Both platforms perform similarly")
            print("   💰 PythonAnywhere is more cost-effective")
            print("   📈 Recommendation: Choose based on budget and features")

def main():
    """Main comparison function"""
    print("🧪 Hosting Platform Comparison Tool")
    print("=" * 80)
    print("This will test both Render and PythonAnywhere with the same load")
    print("=" * 80)
    
    comparator = HostingComparison()
    
    # Test scenarios
    print("📋 Test scenarios:")
    print("   1. Light load (10, 25, 50 users)")
    print("   2. Medium load (25, 50, 100 users)")
    print("   3. Heavy load (50, 100, 200 users)")
    print("   4. Custom test")
    
    try:
        choice = input("\nSelect test scenario (1-4): ").strip()
        
        if choice == "1":
            user_counts = [10, 25, 50]
        elif choice == "2":
            user_counts = [25, 50, 100]
        elif choice == "3":
            user_counts = [50, 100, 200]
        elif choice == "4":
            user_input = input("Enter user counts (comma-separated, e.g., 10,25,50): ")
            user_counts = [int(x.strip()) for x in user_input.split(',')]
        else:
            print("Invalid choice. Using light load...")
            user_counts = [10, 25, 50]
        
        print(f"\n⚠️  WARNING: This will test both sites with {max(user_counts)} concurrent users!")
        confirm = input("Continue? (yes/no): ").lower()
        
        if confirm == 'yes':
            results = comparator.compare_sites(user_counts)
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hosting_comparison_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"\n📄 Detailed results saved to: {filename}")
        else:
            print("Test cancelled.")
            
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
