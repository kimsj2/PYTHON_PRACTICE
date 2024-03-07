import ray
import pandas as pd
import time
# Ray를 초기화합니다.
ray.init(num_cpus=16)

# 병렬로 계산될 함수를 정의합니다.
@ray.remote
def complex_computation(data):
    # 여기서는 간단한 예시로 각 요소를 제곱하는 연산을 수행합니다.
    result = [x**2 for x in data]
    return result

start = time.time()

# 데이터를 분할합니다.
data = [list(range(100)), list(range(100, 200)), list(range(200, 300))]

# 병렬로 각 데이터에 대한 연산을 수행합니다.
futures = [complex_computation.remote(d) for d in data]

# 결과를 수집합니다.
results = ray.get(futures)

# DataFrame으로 변환합니다.
dfs = [pd.DataFrame({'data': d, 'result': r}) for d, r in zip(data, results)]

# DataFrame을 합쳐줍니다.
final_df = pd.concat(dfs)

end = time.time()
# 결과를 출력합니다.
print(final_df)
print(f'총 걸린시간 - {end-start}')
# Ray를 종료합니다.
ray.shutdown()
