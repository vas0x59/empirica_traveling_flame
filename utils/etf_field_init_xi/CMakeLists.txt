
cmake_minimum_required(VERSION 3.20 FATAL_ERROR)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
set(CMAKE_XCODE_GENERATE_SCHEME TRUE)  

project(etf_field_init_xi LANGUAGES CXX C)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# =====================================================================================
#             OpenFOAM configurations: elegant way!
# -------------------------------------------------------------------------------------
include(OpenFOAM)
# =====================================================================================
#             Include path configuration, similar to that in Make/options
include_directories(${OpenFOAM_SRC}/meshTools/lnInclude)
# =====================================================================================
set(PATH_SRC "src")

# add_subdirectory(${PATH_SRC})
include_directories(${PATH_SRC})

add_executable(${PROJECT_NAME} ${PATH_SRC}/etf_field_init_xi.C)

# dynamic link
target_link_libraries(${PROJECT_NAME} OpenFOAM dl m Pstream finiteVolume  meshTools)

# # =====================================================================================
# #             XCode scheme configurations
# # -------------------------------------------------------------------------------------
# if (CMAKE_GENERATOR MATCHES "Xcode")
#     message(STATUS "Set xcode scheme-run-arguments")
#     set_property (TARGET ${PROJECT_NAME} PROPERTY XCODE_SCHEME_ARGUMENTS "-case ${CMAKE_SOURCE_DIR}/testCase")
#     set_property(TARGET ${PROJECT_NAME} PROPERTY XCODE_SCHEME_ENVIRONMENT WM_PROJECT_DIR=$ENV{WM_PROJECT_DIR} WM_PROJECT=$ENV{WM_PROJECT} WM_PROJECT_VERSION=$ENV{WM_PROJECT_VERSION})
# endif ()
# =====================================================================================
# ======================= Message out ===========================
message(STATUS "Configuration type: " ${CMAKE_CONFIGURATION_TYPES})