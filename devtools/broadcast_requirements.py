import yaml

def heal(arg):

    output = []

    for ii in arg:
        if type(ii) is list:
            for jj in ii:
                if type(jj) is list:
                    for kk in jj:
                        if type(kk) is list:
                            for ll in kk:
                                if ll not in output:
                                    output.append(ll)
                        else:
                            if kk not in output:
                                output.append(kk)
                else:
                    if jj not in output:
                        output.append(jj)
        else:
            if ii not in output:
                output.append(ii)

    return output

with open('requirements.yaml') as fff:
    all_requirements = yaml.load(fff, Loader=yaml.FullLoader)

# Broadcasting to conda-build

## meta.yaml

print(" ")
print("# Broadcasting to conda-build")
print(" ")

with open('conda-build/meta.yaml') as fff:
    meta = yaml.load(fff, Loader=yaml.FullLoader)

meta["requirements"]["build"] = heal(all_requirements["setup"]["dependencies"])
meta["requirements"]["run"] = heal(all_requirements["production"]["dependencies"])

fff = open("conda-build/meta.yaml", "w")
yaml.dump(meta, fff, sort_keys=False)
fff.close()

with open("conda-build/meta.yaml", "r") as fff:
    meta_lines = fff.readlines()

with open("conda-build/meta.yaml", "w") as fff:
    for line in meta_lines:
        if line.startswith('  version:'):
            line = '  version: \"{{ environ[\'GIT_DESCRIBE_TAG\'] }}\"\n'
        fff.write(line)

print("conda-build/meta.yaml... updated")

# Broadcasting to conda-envs

print(" ")
print("# Broadcasting to conda-envs")
print(" ")

## Production

env_dict={}
env_dict["channels"]=heal(all_requirements["production"]["channels"])
env_dict["dependencies"]=heal(all_requirements["production"]["dependencies"])
fff = open("conda-envs/production_env.yaml", "w")
yaml.dump(env_dict, fff, sort_keys=False)
fff.close()

print("conda-envs/production_env.yaml... updated")

## Development

env_dict={}
env_dict["channels"]=heal(all_requirements["development"]["channels"])
env_dict["dependencies"]=heal(all_requirements["development"]["dependencies"])
fff = open("conda-envs/development_env.yaml", "w")
yaml.dump(env_dict, fff, sort_keys=False)
fff.close()

print("conda-envs/development_env.yaml... updated")

## Test

env_dict={}
env_dict["channels"]=heal(all_requirements["test"]["channels"])
env_dict["dependencies"]=heal(all_requirements["test"]["dependencies"])
fff = open("conda-envs/test_env.yaml", "w")
yaml.dump(env_dict, fff, sort_keys=False)
fff.close()

print("conda-envs/test_env.yaml... updated")

## Docs

env_dict={}
env_dict["channels"]=heal(all_requirements["docs"]["channels"])
env_dict["dependencies"]=heal(all_requirements["docs"]["dependencies"])
fff = open("conda-envs/docs_env.yaml", "w")
yaml.dump(env_dict, fff, sort_keys=False)
fff.close()

print("conda-envs/docs_env.yaml... updated")

## Setup

env_dict={}
env_dict["channels"]=heal(all_requirements["setup"]["channels"])
env_dict["dependencies"]=heal(all_requirements["setup"]["dependencies"])
fff = open("conda-envs/setup_env.yaml", "w")
yaml.dump(env_dict, fff, sort_keys=False)
fff.close()

print("conda-envs/setup_env.yaml... updated")

## Build

env_dict={}
env_dict["channels"]=heal(all_requirements["conda-build"]["channels"])
env_dict["dependencies"]=heal(all_requirements["conda-build"]["dependencies"])
fff = open("conda-envs/build_env.yaml", "w")
yaml.dump(env_dict, fff, sort_keys=False)
fff.close()

print("conda-envs/build_env.yaml... updated")

print(" ")
